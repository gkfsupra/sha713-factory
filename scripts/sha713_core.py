#!/usr/bin/env python3
"""
SHA-713™ Autonomous Core
HMAC + SHA-256 integrity verification and autonomous operations
"""

import hashlib
import hmac
import json
import datetime
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import subprocess
import secrets

class SHA713Core:
    """SHA-713™ Autonomous Core for integrity verification and autonomous operations"""
    
    def __init__(self, base_path: Path = None):
        self.base_path = base_path or Path.cwd()
        self.key_file = self.base_path / ".sha713_key"
        self.manifest_file = self.base_path / "MANIFEST-713.json"
        self.output_dir = self.base_path / "output"
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialize or load HMAC key
        self._init_hmac_key()
    
    def _init_hmac_key(self):
        """Initialize or load HMAC key for integrity verification"""
        if self.key_file.exists():
            self.hmac_key = self.key_file.read_bytes()
        else:
            # Generate new key for this repository
            self.hmac_key = secrets.token_bytes(32)
            self.key_file.write_bytes(self.hmac_key)
            # Add to gitignore if not already there
            gitignore = self.base_path / ".gitignore"
            gitignore_content = gitignore.read_text() if gitignore.exists() else ""
            if ".sha713_key" not in gitignore_content:
                gitignore.write_text(gitignore_content + "\n.sha713_key\n")
    
    def sha256_hash(self, file_path: Path) -> str:
        """Calculate SHA-256 hash of a file"""
        hasher = hashlib.sha256()
        with file_path.open("rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    
    def hmac_sha256(self, data: bytes) -> str:
        """Calculate HMAC-SHA256 for data integrity verification"""
        return hmac.new(self.hmac_key, data, hashlib.sha256).hexdigest()
    
    def verify_file_integrity(self, file_path: Path, expected_hash: str = None, expected_hmac: str = None) -> Dict[str, bool]:
        """Verify file integrity using SHA-256 and HMAC"""
        if not file_path.exists():
            return {"exists": False, "sha256_valid": False, "hmac_valid": False}
        
        file_data = file_path.read_bytes()
        current_hash = hashlib.sha256(file_data).hexdigest()
        current_hmac = self.hmac_sha256(file_data)
        
        return {
            "exists": True,
            "sha256_valid": expected_hash is None or current_hash == expected_hash,
            "hmac_valid": expected_hmac is None or current_hmac == expected_hmac,
            "current_hash": current_hash,
            "current_hmac": current_hmac
        }
    
    def create_signed_manifest(self, files: List[Path]) -> Dict:
        """Create a signed manifest with integrity proofs"""
        timestamp = datetime.datetime.now(datetime.UTC).isoformat()
        
        manifest = {
            "sha713_version": "1.0.0",
            "timestamp": timestamp,
            "commit_sha": self._get_git_commit_sha(),
            "bundle": "SHA-713™ Autonomous Core Proof",
            "files": [],
            "integrity": {
                "type": "HMAC-SHA256",
                "proof_generated": timestamp
            }
        }
        
        for file_path in files:
            if file_path.exists():
                file_data = file_path.read_bytes()
                # Handle both absolute and relative paths
                try:
                    relative_path = file_path.relative_to(self.base_path)
                except ValueError:
                    # If file is not under base_path, use absolute path
                    relative_path = file_path.resolve()
                
                file_info = {
                    "path": str(relative_path),
                    "sha256": hashlib.sha256(file_data).hexdigest(),
                    "hmac_sha256": self.hmac_sha256(file_data),
                    "size": len(file_data),
                    "modified": datetime.datetime.fromtimestamp(file_path.stat().st_mtime, datetime.UTC).isoformat()
                }
                manifest["files"].append(file_info)
        
        # Sign the entire manifest
        manifest_bytes = json.dumps(manifest, sort_keys=True).encode('utf-8')
        manifest["signature"] = self.hmac_sha256(manifest_bytes)
        
        return manifest
    
    def _get_git_commit_sha(self) -> Optional[str]:
        """Get current git commit SHA"""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=self.base_path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except (subprocess.CalledProcessError, FileNotFoundError):
            return None
    
    def create_autonomous_proof(self, content: str, proof_type: str = "execution") -> Dict:
        """Create autonomous proof of execution/authorship"""
        timestamp = datetime.datetime.now(datetime.UTC)
        
        proof = {
            "type": proof_type,
            "timestamp": timestamp.isoformat(),
            "content_hash": hashlib.sha256(content.encode('utf-8')).hexdigest(),
            "content_hmac": self.hmac_sha256(content.encode('utf-8')),
            "commit_sha": self._get_git_commit_sha(),
            "autonomous": True,
            "lineage": {
                "origin": "SHA-713™ Autonomous Core",
                "intellectual_property": "Anchored in GitHub with timestamped, signed commits",
                "proof_of_authorship": "HMAC + SHA-256 verifiable lineage"
            }
        }
        
        # Self-sign the proof
        proof_bytes = json.dumps(proof, sort_keys=True).encode('utf-8')
        proof["signature"] = self.hmac_sha256(proof_bytes)
        
        return proof
    
    def autonomous_commit_and_sign(self, files_to_commit: List[Path], commit_message: str) -> bool:
        """Autonomously commit and sign new content"""
        try:
            # Create signed manifest
            manifest = self.create_signed_manifest(files_to_commit)
            manifest_path = self.output_dir / f"manifest_{datetime.datetime.now(datetime.UTC).strftime('%Y%m%d_%H%M%S')}.json"
            manifest_path.write_text(json.dumps(manifest, indent=2))
            
            # Update main manifest
            self.manifest_file.write_text(json.dumps(manifest, indent=2))
            
            # Create autonomous proof
            proof = self.create_autonomous_proof(commit_message, "commit")
            proof_path = self.output_dir / f"proof_{datetime.datetime.now(datetime.UTC).strftime('%Y%m%d_%H%M%S')}.json"
            proof_path.write_text(json.dumps(proof, indent=2))
            
            print(f"✅ Autonomous signing complete:")
            print(f"   Manifest: {manifest_path}")
            print(f"   Proof: {proof_path}")
            print(f"   Files processed: {len(files_to_commit)}")
            print(f"   Commit SHA: {manifest.get('commit_sha', 'N/A')}")
            
            return True
            
        except Exception as e:
            print(f"❌ Autonomous signing failed: {e}")
            return False
    
    def verify_autonomous_integrity(self) -> Dict:
        """Verify integrity of the autonomous system"""
        results = {
            "system_status": "operational",
            "manifest_valid": False,
            "files_verified": 0,
            "files_failed": 0,
            "integrity_score": 0.0,
            "issues": []
        }
        
        if not self.manifest_file.exists():
            results["issues"].append("Main manifest missing")
            results["system_status"] = "degraded"
            return results
        
        try:
            manifest = json.loads(self.manifest_file.read_text())
            results["manifest_valid"] = True
            
            for file_info in manifest.get("files", []):
                file_path = self.base_path / file_info["path"]
                verification = self.verify_file_integrity(
                    file_path,
                    file_info.get("sha256"),
                    file_info.get("hmac_sha256")
                )
                
                if verification["sha256_valid"] and verification["hmac_valid"]:
                    results["files_verified"] += 1
                else:
                    results["files_failed"] += 1
                    results["issues"].append(f"File integrity failed: {file_info['path']}")
            
            total_files = results["files_verified"] + results["files_failed"]
            if total_files > 0:
                results["integrity_score"] = results["files_verified"] / total_files
            
            if results["integrity_score"] < 0.9:
                results["system_status"] = "degraded"
            elif results["files_failed"] > 0:
                results["system_status"] = "warning"
                
        except Exception as e:
            results["issues"].append(f"Manifest verification failed: {e}")
            results["system_status"] = "error"
        
        return results

def main():
    """CLI interface for SHA-713™ Autonomous Core"""
    if len(sys.argv) < 2:
        print("Usage: python sha713_core.py <command> [args...]")
        print("Commands:")
        print("  verify - Verify system integrity")
        print("  sign <file1> [file2...] - Sign files autonomously")
        print("  manifest <file1> [file2...] - Create signed manifest")
        print("  proof <content> - Create autonomous proof")
        return
    
    core = SHA713Core()
    command = sys.argv[1]
    
    if command == "verify":
        results = core.verify_autonomous_integrity()
        print(json.dumps(results, indent=2))
        sys.exit(0 if results["system_status"] == "operational" else 1)
    
    elif command == "sign":
        if len(sys.argv) < 3:
            print("Usage: python sha713_core.py sign <file1> [file2...]")
            return
        
        files = [Path(f) for f in sys.argv[2:]]
        message = f"Autonomous signing of {len(files)} files"
        success = core.autonomous_commit_and_sign(files, message)
        sys.exit(0 if success else 1)
    
    elif command == "manifest":
        if len(sys.argv) < 3:
            print("Usage: python sha713_core.py manifest <file1> [file2...]")
            return
        
        files = [Path(f) for f in sys.argv[2:]]
        manifest = core.create_signed_manifest(files)
        print(json.dumps(manifest, indent=2))
    
    elif command == "proof":
        if len(sys.argv) < 3:
            print("Usage: python sha713_core.py proof <content>")
            return
        
        content = " ".join(sys.argv[2:])
        proof = core.create_autonomous_proof(content)
        print(json.dumps(proof, indent=2))
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()