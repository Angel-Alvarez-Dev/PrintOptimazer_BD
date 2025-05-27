# scripts/health_check.py
"""
Comprehensive health check script
"""
import asyncio
import aiohttp
import psutil
import subprocess
import time
import sys
from pathlib import Path
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HealthChecker:
    def __init__(self, config_file="health_check_config.json"):
        self.config = self.load_config(config_file)
        self.results = {}
    
    def load_config(self, config_file):
        """Load health check configuration"""
        default_config = {
            "api_url": "http://localhost:8000",
            "database_url": "postgresql://user:pass@localhost:5432/db",
            "redis_url": "redis://localhost:6379/0",
            "thresholds": {
                "cpu_percent": 90,
                "memory_percent": 90,
                "disk_percent": 95,
                "response_time_ms": 5000
            },
            "endpoints": [
                "/health",
                "/api/v1/auth/login",
                "/api/v1/projects/",
                "/api/v1/materials/"
            ]
        }
        
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            return {**default_config, **config}
        except FileNotFoundError:
            return default_config
    
    def check_system_health(self):
        """Check system resource health"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            self.results['system'] = {
                'status': 'healthy',
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'disk_percent': (disk.used / disk.total) * 100,
                'load_average': os.getloadavg() if hasattr(os, 'getloadavg') else None
            }
            
            # Check thresholds
            if cpu_percent > self.config['thresholds']['cpu_percent']:
                self.results['system']['status'] = 'unhealthy'
                self.results['system']['issues'] = self.results['system'].get('issues', [])
                self.results['system']['issues'].append(f"High CPU usage: {cpu_percent}%")
            
            if memory.percent > self.config['thresholds']['memory_percent']:
                self.results['system']['status'] = 'unhealthy'
                self.results['system']['issues'] = self.results['system'].get('issues', [])
                self.results['system']['issues'].append(f"High memory usage: {memory.percent}%")
            
            disk_percent = (disk.used / disk.total) * 100
            if disk_percent > self.config['thresholds']['disk_percent']:
                self.results['system']['status'] = 'unhealthy'
                self.results['system']['issues'] = self.results['system'].get('issues', [])
                self.results['system']['issues'].append(f"High disk usage: {disk_percent}%")
            
        except Exception as e:
            self.results['system'] = {
                'status': 'error',
                'error': str(e)
            }
    
    async def check_api_health(self):
        """Check API endpoint health"""
        try:
            async with aiohttp.ClientSession() as session:
                endpoint_results = {}
                
                for endpoint in self.config['endpoints']:
                    try:
                        start_time = time.time()
                        
                        async with session.get(
                            f"{self.config['api_url']}{endpoint}",
                            timeout=aiohttp.ClientTimeout(total=10)
                        ) as response:
                            response_time = (time.time() - start_time) * 1000
                            
                            endpoint_results[endpoint] = {
                                'status': 'healthy' if response.status < 400 else 'unhealthy',
                                'http_status': response.status,
                                'response_time_ms': response_time
                            }
                            
                            if response_time > self.config['thresholds']['response_time_ms']:
                                endpoint_results[endpoint]['status'] = 'slow'
                                endpoint_results[endpoint]['warning'] = f"Slow response: {response_time:.0f}ms"
                    
                    except asyncio.TimeoutError:
                        endpoint_results[endpoint] = {
                            'status': 'timeout',
                            'error': 'Request timeout'
                        }
                    except Exception as e:
                        endpoint_results[endpoint] = {
                            'status': 'error',
                            'error': str(e)
                        }
                
                # Overall API status
                healthy_endpoints = sum(1 for r in endpoint_results.values() if r['status'] == 'healthy')
                total_endpoints = len(endpoint_results)
                
                self.results['api'] = {
                    'status': 'healthy' if healthy_endpoints == total_endpoints else 'degraded',
                    'healthy_endpoints': healthy_endpoints,
                    'total_endpoints': total_endpoints,
                    'endpoints': endpoint_results
                }
                
        except Exception as e:
            self.results['api'] = {
                'status': 'error',
                'error': str(e)
            }
    
    def check_database_health(self):
        """Check database health"""
        try:
            # Simple connection test
            result = subprocess.run(
                ['psql', self.config['database_url'], '-c', 'SELECT 1;'],
                capture_output=True,
                timeout=10,
                text=True
            )
            
            if result.returncode == 0:
                self.results['database'] = {
                    'status': 'healthy',
                    'connection': 'ok'
                }
            else:
                self.results['database'] = {
                    'status': 'unhealthy',
                    'connection': 'failed',
                    'error': result.stderr
                }
                
        except subprocess.TimeoutExpired:
            self.results['database'] = {
                'status': 'timeout',
                'error': 'Connection timeout'
            }
        except Exception as e:
            self.results['database'] = {
                'status': 'error',
                'error': str(e)
            }
    
    def check_redis_health(self):
        """Check Redis health"""
        try:
            import redis
            
            r = redis.from_url(self.config['redis_url'])
            
            # Test basic operations
            test_key = "health_check_test"
            r.set(test_key, "test_value", ex=60)
            value = r.get(test_key)
            r.delete(test_key)
            
            if value == b"test_value":
                self.results['redis'] = {
                    'status': 'healthy',
                    'connection': 'ok',
                    'operations': 'ok'
                }
            else:
                self.results['redis'] = {
                    'status': 'unhealthy',
                    'connection': 'ok',
                    'operations': 'failed'
                }
                
        except Exception as e:
            self.results['redis'] = {
                'status': 'error',
                'error': str(e)
            }
    
    def check_docker_health(self):
        """Check Docker containers health"""
        try:
            result = subprocess.run(
                ['docker', 'ps', '--format', 'json'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                containers = []
                for line in result.stdout.strip().split('\n'):
                    if line:
                        container = json.loads(line)
                        if 'printoptimizer' in container.get('Names', '').lower():
                            containers.append({
                                'name': container['Names'],
                                'status': container['Status'],
                                'healthy': container['Status'].startswith('Up')
                            })
                
                healthy_containers = sum(1 for c in containers if c['healthy'])
                
                self.results['docker'] = {
                    'status': 'healthy' if healthy_containers == len(containers) else 'degraded',
                    'containers': containers,
                    'healthy_count': healthy_containers,
                    'total_count': len(containers)
                }
            else:
                self.results['docker'] = {
                    'status': 'error',
                    'error': result.stderr
                }
                
        except Exception as e:
            self.results['docker'] = {
                'status': 'error',
                'error': str(e)
            }
    
    async def run_all_checks(self):
        """Run all health checks"""
        logger.info("Running comprehensive health check...")
        
        # System checks
        self.check_system_health()
        
        # API checks
        await self.check_api_health()
        
        # Database checks
        self.check_database_health()
        
        # Redis checks
        self.check_redis_health()
        
        # Docker checks
        self.check_docker_health()
        
        # Overall status
        all_statuses = [check.get('status', 'unknown') for check in self.results.values()]
        
        if all(status == 'healthy' for status in all_statuses):
            overall_status = 'healthy'
        elif any(status in ['error', 'timeout'] for status in all_statuses):
            overall_status = 'critical'
        else:
            overall_status = 'degraded'
        
        self.results['overall'] = {
            'status': overall_status,
            'timestamp': time.time(),
            'summary': {
                'healthy': sum(1 for s in all_statuses if s == 'healthy'),
                'degraded': sum(1 for s in all_statuses if s in ['degraded', 'slow']),
                'critical': sum(1 for s in all_statuses if s in ['error', 'timeout', 'unhealthy'])
            }
        }
        
        return self.results
    
    def print_results(self):
        """Print health check results in a readable format"""
        print("\n" + "="*60)
        print("PRINTOPTIMIZER HEALTH CHECK RESULTS")
        print("="*60)
        
        for component, result in self.results.items():
            if component == 'overall':
                continue
                
            status = result.get('status', 'unknown').upper()
            status_color = {
                'HEALTHY': '\033[92m',  # Green
                'DEGRADED': '\033[93m',  # Yellow
                'UNHEALTHY': '\033[91m',  # Red
                'ERROR': '\033[91m',     # Red
                'TIMEOUT': '\033[91m',   # Red
            }.get(status, '\033[0m')  # Default
            
            print(f"\n{component.upper()}: {status_color}{status}\033[0m")
            
            if 'error' in result:
                print(f"  Error: {result['error']}")
            elif 'issues' in result:
                for issue in result['issues']:
                    print(f"  Issue: {issue}")
            elif component == 'api' and 'endpoints' in result:
                for endpoint, endpoint_result in result['endpoints'].items():
                    endpoint_status = endpoint_result['status'].upper()
                    print(f"  {endpoint}: {endpoint_status}")
                    if 'response_time_ms' in endpoint_result:
                        print(f"    Response time: {endpoint_result['response_time_ms']:.0f}ms")
        
        # Overall summary
        overall = self.results.get('overall', {})
        overall_status = overall.get('status', 'unknown').upper()
        status_color = {
            'HEALTHY': '\033[92m',
            'DEGRADED': '\033[93m', 
            'CRITICAL': '\033[91m',
        }.get(overall_status, '\033[0m')
        
        print(f"\n{'='*60}")
        print(f"OVERALL STATUS: {status_color}{overall_status}\033[0m")
        
        if 'summary' in overall:
            summary = overall['summary']
            print(f"Healthy: {summary['healthy']}, Degraded: {summary['degraded']}, Critical: {summary['critical']}")
        
        print("="*60)

async def main():
    """Main health check function"""
    checker = HealthChecker()
    results = await checker.run_all_checks()
    
    # Print results
    checker.print_results()
    
    # Save results to file
    output_file = f"health_check_{int(time.time())}.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    # Exit with appropriate code
    overall_status = results.get('overall', {}).get('status', 'unknown')
    if overall_status == 'healthy':
        sys.exit(0)
    elif overall_status == 'degraded':
        sys.exit(1)
    else:  # critical
        sys.exit(2)

if __name__ == "__main__":
    asyncio.run(main())