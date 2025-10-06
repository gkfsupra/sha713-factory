#!/usr/bin/env python3
"""
SHA-713™ Real-time Notification System
Handles notifications to Codex and other external systems
"""

import json
import requests
import hmac
import hashlib
import datetime
from pathlib import Path
from typing import Dict, List, Optional
import os
import sys

class SHA713NotificationSystem:
    """Real-time notification system for SHA-713™ autonomous operations"""
    
    def __init__(self, base_path: Path = None):
        self.base_path = base_path or Path.cwd()
        self.config_file = self.base_path / "config" / "notification_config.json"
        self.log_file = self.base_path / "output" / "notification_log.json"
        self.config = self._load_config()
        
    def _load_config(self) -> Dict:
        """Load notification configuration"""
        default_config = {
            "codex": {
                "enabled": True,
                "webhook_url": os.getenv("SHA713_CODEX_WEBHOOK"),
                "verify_ssl": True,
                "timeout": 30
            },
            "dashboard": {
                "enabled": True,
                "api_endpoint": os.getenv("SHA713_DASHBOARD_API"),
                "api_key": os.getenv("SHA713_DASHBOARD_KEY")
            },
            "external_apis": {
                "enabled": True,
                "endpoints": []
            },
            "marketing_automation": {
                "enabled": True,
                "social_media": False,
                "blog_updates": False
            }
        }
        
        if self.config_file.exists():
            try:
                file_config = json.loads(self.config_file.read_text())
                # Merge with defaults
                for key, value in file_config.items():
                    if key in default_config:
                        default_config[key].update(value)
                    else:
                        default_config[key] = value
            except Exception as e:
                print(f"Warning: Could not load config file: {e}")
        
        return default_config
    
    def _create_notification_payload(self, event_type: str, data: Dict) -> Dict:
        """Create standardized notification payload"""
        timestamp = datetime.datetime.now(datetime.UTC).isoformat()
        
        payload = {
            "sha713_event": {
                "type": event_type,
                "timestamp": timestamp,
                "version": "1.0.0",
                "autonomous": True
            },
            "repository": {
                "name": data.get("repository", "sha713-factory"),
                "commit_sha": data.get("commit_sha"),
                "branch": data.get("branch", "main")
            },
            "verification": {
                "status": data.get("verification_status", "unknown"),
                "integrity_score": data.get("integrity_score", 0.0),
                "files_verified": data.get("files_verified", 0),
                "proof_type": "HMAC-SHA256"
            },
            "strategic_signals": {
                "technical_authority": "autonomous_ai_deployment",
                "ip_protection": "timestamped_signed_commits",
                "operational_excellence": "zero_effort_scalability",
                "market_position": "top_percentile_systems"
            },
            "metadata": {
                "lineage_proof": "SHA-713™ Autonomous Core",
                "execution_id": data.get("execution_id"),
                "artifacts_available": True
            }
        }
        
        # Add HMAC signature for verification
        payload_bytes = json.dumps(payload, sort_keys=True).encode('utf-8')
        signature = self._sign_payload(payload_bytes)
        payload["signature"] = signature
        
        return payload
    
    def _sign_payload(self, payload_bytes: bytes) -> str:
        """Sign notification payload with HMAC"""
        # Use repository-specific key or environment variable
        key = os.getenv("SHA713_NOTIFICATION_KEY", "sha713-default-key").encode('utf-8')
        return hmac.new(key, payload_bytes, hashlib.sha256).hexdigest()
    
    def notify_codex(self, payload: Dict) -> bool:
        """Send notification to Codex system"""
        if not self.config["codex"]["enabled"]:
            self._log_notification("codex", "skipped", "Codex notifications disabled")
            return True
        
        webhook_url = self.config["codex"]["webhook_url"]
        if not webhook_url:
            self._log_notification("codex", "skipped", "No webhook URL configured")
            return True
        
        try:
            # Prepare Codex-specific payload
            codex_payload = {
                "source": "sha713_autonomous_core",
                "event": "autonomous_execution",
                "data": payload,
                "requires_indexing": True,
                "priority": "high"
            }
            
            response = requests.post(
                webhook_url,
                json=codex_payload,
                headers={
                    "Content-Type": "application/json",
                    "X-SHA713-Signature": payload.get("signature", ""),
                    "User-Agent": "SHA713-Autonomous-Core/1.0"
                },
                timeout=self.config["codex"]["timeout"],
                verify=self.config["codex"]["verify_ssl"]
            )
            
            response.raise_for_status()
            self._log_notification("codex", "success", f"Status: {response.status_code}")
            return True
            
        except Exception as e:
            self._log_notification("codex", "error", str(e))
            return False
    
    def notify_dashboard(self, payload: Dict) -> bool:
        """Send notification to dashboard API"""
        if not self.config["dashboard"]["enabled"]:
            self._log_notification("dashboard", "skipped", "Dashboard notifications disabled")
            return True
        
        api_endpoint = self.config["dashboard"]["api_endpoint"]
        api_key = self.config["dashboard"]["api_key"]
        
        if not api_endpoint or not api_key:
            self._log_notification("dashboard", "skipped", "Dashboard API not configured")
            return True
        
        try:
            # Prepare dashboard-specific payload
            dashboard_payload = {
                "event_type": "sha713_autonomous_update",
                "metrics": {
                    "integrity_score": payload["verification"]["integrity_score"],
                    "verification_status": payload["verification"]["status"],
                    "autonomous_execution": True,
                    "timestamp": payload["sha713_event"]["timestamp"]
                },
                "strategic_update": payload["strategic_signals"],
                "repository_data": payload["repository"]
            }
            
            response = requests.post(
                f"{api_endpoint}/v1/sha713/updates",
                json=dashboard_payload,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                    "X-SHA713-Source": "autonomous-core"
                },
                timeout=30
            )
            
            response.raise_for_status()
            self._log_notification("dashboard", "success", f"Status: {response.status_code}")
            return True
            
        except Exception as e:
            self._log_notification("dashboard", "error", str(e))
            return False
    
    def notify_external_apis(self, payload: Dict) -> bool:
        """Send notifications to configured external APIs"""
        if not self.config["external_apis"]["enabled"]:
            self._log_notification("external_apis", "skipped", "External API notifications disabled")
            return True
        
        endpoints = self.config["external_apis"]["endpoints"]
        if not endpoints:
            self._log_notification("external_apis", "skipped", "No external endpoints configured")
            return True
        
        success_count = 0
        for endpoint in endpoints:
            try:
                response = requests.post(
                    endpoint["url"],
                    json=payload,
                    headers=endpoint.get("headers", {}),
                    timeout=endpoint.get("timeout", 30)
                )
                response.raise_for_status()
                success_count += 1
                self._log_notification("external_api", "success", f"Endpoint: {endpoint['url']}")
            except Exception as e:
                self._log_notification("external_api", "error", f"Endpoint: {endpoint['url']}, Error: {e}")
        
        return success_count == len(endpoints)
    
    def trigger_marketing_automation(self, payload: Dict) -> bool:
        """Trigger marketing automation based on autonomous updates"""
        if not self.config["marketing_automation"]["enabled"]:
            self._log_notification("marketing", "skipped", "Marketing automation disabled")
            return True
        
        try:
            # Create marketing event
            marketing_event = {
                "event": "autonomous_technical_achievement",
                "timestamp": payload["sha713_event"]["timestamp"],
                "achievements": [
                    "Autonomous AI deployment executed",
                    "IP protection verified with timestamped commits",
                    "Zero-effort scalability demonstrated",
                    "Top percentile autonomous systems operational"
                ],
                "metrics": {
                    "integrity_score": payload["verification"]["integrity_score"],
                    "autonomous_execution": True
                },
                "content_suggestions": [
                    "Technical authority in autonomous AI systems",
                    "Operational excellence in self-validating workflows",
                    "Market leadership in verifiable AI deployment"
                ]
            }
            
            # Save marketing event for later processing
            marketing_file = self.base_path / "output" / f"marketing_event_{datetime.datetime.now(datetime.UTC).strftime('%Y%m%d_%H%M%S')}.json"
            marketing_file.write_text(json.dumps(marketing_event, indent=2))
            
            self._log_notification("marketing", "success", f"Event saved: {marketing_file}")
            return True
            
        except Exception as e:
            self._log_notification("marketing", "error", str(e))
            return False
    
    def _log_notification(self, system: str, status: str, details: str):
        """Log notification attempt"""
        log_entry = {
            "timestamp": datetime.datetime.now(datetime.UTC).isoformat(),
            "system": system,
            "status": status,
            "details": details
        }
        
        # Ensure output directory exists
        self.log_file.parent.mkdir(exist_ok=True)
        
        # Append to log file
        logs = []
        if self.log_file.exists():
            try:
                logs = json.loads(self.log_file.read_text())
            except:
                logs = []
        
        logs.append(log_entry)
        
        # Keep only last 100 entries
        logs = logs[-100:]
        
        self.log_file.write_text(json.dumps(logs, indent=2))
        
        # Also print to console
        print(f"📡 {system.upper()}: {status} - {details}")
    
    def send_all_notifications(self, event_type: str, data: Dict) -> Dict[str, bool]:
        """Send notifications to all configured systems"""
        payload = self._create_notification_payload(event_type, data)
        
        results = {
            "codex": self.notify_codex(payload),
            "dashboard": self.notify_dashboard(payload),
            "external_apis": self.notify_external_apis(payload),
            "marketing": self.trigger_marketing_automation(payload)
        }
        
        # Save complete payload for reference
        payload_file = self.base_path / "output" / f"notification_payload_{datetime.datetime.now(datetime.UTC).strftime('%Y%m%d_%H%M%S')}.json"
        payload_file.write_text(json.dumps(payload, indent=2))
        
        success_count = sum(results.values())
        total_count = len(results)
        
        print(f"🔔 Notification Summary: {success_count}/{total_count} systems notified successfully")
        return results

def main():
    """CLI interface for SHA-713™ Notification System"""
    if len(sys.argv) < 2:
        print("Usage: python sha713_notifications.py <command> [args...]")
        print("Commands:")
        print("  notify <event_type> - Send notifications with data from stdin")
        print("  test - Test all notification endpoints")
        print("  config - Show current configuration")
        return
    
    notifier = SHA713NotificationSystem()
    command = sys.argv[1]
    
    if command == "notify":
        if len(sys.argv) < 3:
            print("Usage: python sha713_notifications.py notify <event_type>")
            return
        
        event_type = sys.argv[2]
        
        # Read data from stdin if available
        data = {}
        if not sys.stdin.isatty():
            try:
                data = json.loads(sys.stdin.read())
            except:
                pass
        
        results = notifier.send_all_notifications(event_type, data)
        print(json.dumps(results, indent=2))
        sys.exit(0 if all(results.values()) else 1)
    
    elif command == "test":
        test_data = {
            "repository": "sha713-factory",
            "commit_sha": "test-commit",
            "verification_status": "operational",
            "integrity_score": 1.0,
            "files_verified": 5
        }
        
        results = notifier.send_all_notifications("test_notification", test_data)
        print("Test results:", json.dumps(results, indent=2))
    
    elif command == "config":
        print(json.dumps(notifier.config, indent=2))
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()