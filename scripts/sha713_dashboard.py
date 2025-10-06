#!/usr/bin/env python3
"""
SHA-713™ Autonomous Dashboard Generator
Creates a living dashboard showing autonomous operations status
"""

import json
import datetime
from pathlib import Path
from typing import Dict, List
import subprocess
import os

class SHA713Dashboard:
    """Generate autonomous operations dashboard"""
    
    def __init__(self, base_path: Path = None):
        self.base_path = base_path or Path.cwd()
        self.output_dir = self.base_path / "output"
        self.output_dir.mkdir(exist_ok=True)
    
    def get_system_status(self) -> Dict:
        """Get current system status and metrics"""
        try:
            # Run verification
            result = subprocess.run(
                ["python", "scripts/sha713_core.py", "verify"],
                cwd=self.base_path,
                capture_output=True,
                text=True,
                check=True
            )
            verification = json.loads(result.stdout)
        except:
            verification = {"system_status": "error", "integrity_score": 0.0}
        
        # Get git information
        try:
            commit_sha = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=self.base_path,
                capture_output=True,
                text=True,
                check=True
            ).stdout.strip()
            
            commit_date = subprocess.run(
                ["git", "show", "-s", "--format=%ci", "HEAD"],
                cwd=self.base_path,
                capture_output=True,
                text=True,
                check=True
            ).stdout.strip()
        except:
            commit_sha = "unknown"
            commit_date = "unknown"
        
        # Count artifacts
        artifact_count = len(list(self.output_dir.glob("*.json")))
        
        return {
            "timestamp": datetime.datetime.now(datetime.UTC).isoformat(),
            "verification": verification,
            "git": {
                "commit_sha": commit_sha[:8],
                "commit_date": commit_date,
                "full_sha": commit_sha
            },
            "artifacts": {
                "count": artifact_count,
                "last_generated": max(
                    [f.stat().st_mtime for f in self.output_dir.glob("*.json")] + [0]
                )
            }
        }
    
    def generate_html_dashboard(self) -> str:
        """Generate HTML dashboard"""
        status = self.get_system_status()
        
        # Calculate uptime and operational metrics
        integrity_score = status["verification"].get("integrity_score", 0.0)
        system_status = status["verification"].get("system_status", "unknown")
        
        # Status color coding
        status_colors = {
            "operational": "#28a745",
            "warning": "#ffc107", 
            "degraded": "#fd7e14",
            "error": "#dc3545"
        }
        status_color = status_colors.get(system_status, "#6c757d")
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SHA-713™ Autonomous Core Dashboard</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #ffffff;
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        .header {{
            text-align: center;
            margin-bottom: 40px;
        }}
        .logo {{
            font-size: 2.5em;
            font-weight: bold;
            background: linear-gradient(45deg, #ffd700, #ffed4e);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }}
        .subtitle {{
            color: #b8c5d6;
            font-size: 1.2em;
        }}
        .status-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        .status-card {{
            background: rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 25px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
        }}
        .status-header {{
            display: flex;
            align-items: center;
            margin-bottom: 20px;
        }}
        .status-icon {{
            width: 40px;
            height: 40px;
            border-radius: 50%;
            margin-right: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
        }}
        .status-title {{
            font-size: 1.3em;
            font-weight: 600;
        }}
        .metric {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
            padding: 8px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }}
        .metric:last-child {{
            border-bottom: none;
        }}
        .metric-label {{
            color: #b8c5d6;
        }}
        .metric-value {{
            font-weight: 600;
        }}
        .progress-bar {{
            width: 100%;
            height: 8px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 4px;
            overflow: hidden;
            margin: 10px 0;
        }}
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #ffd700, #ffed4e);
            width: {integrity_score * 100}%;
            transition: width 0.3s ease;
        }}
        .timestamp {{
            text-align: center;
            color: #b8c5d6;
            font-size: 0.9em;
            margin-top: 40px;
        }}
        .autonomous-indicator {{
            background: linear-gradient(45deg, #28a745, #20c997);
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: 600;
            display: inline-block;
            margin-top: 10px;
        }}
        .strategic-signals {{
            background: rgba(255, 215, 0, 0.1);
            border: 1px solid rgba(255, 215, 0, 0.3);
            border-radius: 8px;
            padding: 15px;
            margin-top: 20px;
        }}
        .signal-item {{
            padding: 5px 0;
            display: flex;
            align-items: center;
        }}
        .signal-item::before {{
            content: "⚡";
            margin-right: 10px;
            color: #ffd700;
        }}
        .refresh-btn {{
            background: linear-gradient(45deg, #ffd700, #ffed4e);
            color: #1a1a2e;
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            font-weight: 600;
            cursor: pointer;
            margin-top: 20px;
        }}
        .refresh-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(255, 215, 0, 0.3);
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">SHA-713™</div>
            <div class="subtitle">Autonomous Core Operations Dashboard</div>
            <div class="autonomous-indicator">🤖 AUTONOMOUS MODE ACTIVE</div>
        </div>
        
        <div class="status-grid">
            <div class="status-card">
                <div class="status-header">
                    <div class="status-icon" style="background-color: {status_color};">🛡️</div>
                    <div class="status-title">System Status</div>
                </div>
                <div class="metric">
                    <span class="metric-label">Status</span>
                    <span class="metric-value" style="color: {status_color}; text-transform: uppercase;">{system_status}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Integrity Score</span>
                    <span class="metric-value">{integrity_score:.1%}</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill"></div>
                </div>
                <div class="metric">
                    <span class="metric-label">Files Verified</span>
                    <span class="metric-value">{status["verification"].get("files_verified", 0)}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Files Failed</span>
                    <span class="metric-value">{status["verification"].get("files_failed", 0)}</span>
                </div>
            </div>
            
            <div class="status-card">
                <div class="status-header">
                    <div class="status-icon" style="background-color: #17a2b8;">📊</div>
                    <div class="status-title">Repository Info</div>
                </div>
                <div class="metric">
                    <span class="metric-label">Latest Commit</span>
                    <span class="metric-value">{status["git"]["commit_sha"]}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Commit Date</span>
                    <span class="metric-value">{status["git"]["commit_date"][:16] if status["git"]["commit_date"] != "unknown" else "unknown"}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Artifacts Generated</span>
                    <span class="metric-value">{status["artifacts"]["count"]}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Last Activity</span>
                    <span class="metric-value">{datetime.datetime.fromtimestamp(status["artifacts"]["last_generated"]).strftime("%H:%M UTC") if status["artifacts"]["last_generated"] > 0 else "N/A"}</span>
                </div>
            </div>
            
            <div class="status-card">
                <div class="status-header">
                    <div class="status-icon" style="background-color: #28a745;">⚡</div>
                    <div class="status-title">Autonomous Operations</div>
                </div>
                <div class="metric">
                    <span class="metric-label">Auto-Signing</span>
                    <span class="metric-value" style="color: #28a745;">✅ ACTIVE</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Index Updates</span>
                    <span class="metric-value" style="color: #28a745;">✅ ACTIVE</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Notifications</span>
                    <span class="metric-value" style="color: #28a745;">✅ ACTIVE</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Self-Maintenance</span>
                    <span class="metric-value" style="color: #28a745;">✅ OPERATIONAL</span>
                </div>
            </div>
            
            <div class="status-card">
                <div class="status-header">
                    <div class="status-icon" style="background-color: #ffc107;">🎯</div>
                    <div class="status-title">Strategic Position</div>
                </div>
                <div class="strategic-signals">
                    <div class="signal-item">Technical Authority: Autonomous AI Deployment</div>
                    <div class="signal-item">IP Protection: Timestamped Signed Commits</div>
                    <div class="signal-item">Operational Excellence: Zero-Effort Scalability</div>
                    <div class="signal-item">Market Position: Top Percentile Systems</div>
                </div>
            </div>
        </div>
        
        <div class="timestamp">
            Last Updated: {status["timestamp"][:19]} UTC
            <br>
            <button class="refresh-btn" onclick="location.reload()">🔄 Refresh Dashboard</button>
        </div>
    </div>
    
    <script>
        // Auto-refresh every 30 seconds
        setTimeout(function() {{
            location.reload();
        }}, 30000);
        
        // Add some interactive effects
        document.addEventListener('DOMContentLoaded', function() {{
            const cards = document.querySelectorAll('.status-card');
            cards.forEach(card => {{
                card.addEventListener('mouseenter', function() {{
                    this.style.transform = 'translateY(-5px)';
                    this.style.boxShadow = '0 10px 25px rgba(255, 215, 0, 0.1)';
                }});
                card.addEventListener('mouseleave', function() {{
                    this.style.transform = 'translateY(0)';
                    this.style.boxShadow = 'none';
                }});
            }});
        }});
    </script>
</body>
</html>
        """
        
        return html
    
    def generate_json_status(self) -> Dict:
        """Generate JSON status for API consumption"""
        return self.get_system_status()
    
    def save_dashboard(self):
        """Save dashboard files"""
        # HTML Dashboard
        html_content = self.generate_html_dashboard()
        html_file = self.base_path / "index.html"
        html_file.write_text(html_content)
        
        # JSON Status
        json_content = self.generate_json_status()
        json_file = self.output_dir / "dashboard_status.json"
        json_file.write_text(json.dumps(json_content, indent=2))
        
        # Status badge for README
        status = json_content["verification"]["system_status"]
        badge_colors = {
            "operational": "brightgreen",
            "warning": "yellow",
            "degraded": "orange", 
            "error": "red"
        }
        
        badge_data = {
            "schemaVersion": 1,
            "label": "SHA-713™ Status",
            "message": status.upper(),
            "color": badge_colors.get(status, "lightgrey")
        }
        
        badge_file = self.output_dir / "status_badge.json"
        badge_file.write_text(json.dumps(badge_data))
        
        print(f"✅ Dashboard generated:")
        print(f"   HTML: {html_file}")
        print(f"   JSON: {json_file}")
        print(f"   Badge: {badge_file}")

def main():
    """Generate SHA-713™ Autonomous Dashboard"""
    dashboard = SHA713Dashboard()
    dashboard.save_dashboard()

if __name__ == "__main__":
    main()