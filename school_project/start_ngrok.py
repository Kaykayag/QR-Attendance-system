#!/usr/bin/env python
"""
Start ngrok tunnel for Django development server
This script creates an HTTPS tunnel to localhost:8000 for QR code scanning functionality
"""
import os
import sys
from pyngrok import ngrok
import time

def start_ngrok_tunnel():
    """Start ngrok tunnel on port 8000"""
    try:
        # Start ngrok tunnel
        print("🚀 Starting ngrok tunnel...")
        public_url = ngrok.connect(8000, "http")
        
        # Extract the URL
        tunnel_url = str(public_url).replace('<NgrokTunnel: "', '').replace('">', '')
        
        print(f"✅ ngrok tunnel started successfully!")
        print(f"🌐 HTTPS URL: {tunnel_url}")
        print(f"📱 Your QR Attendance System is now accessible at: {tunnel_url}")
        print(f"🔗 Use this URL for camera-based QR scanning on mobile devices")
        print("\n" + "="*60)
        print("⚠️  IMPORTANT: Copy this URL and update your Django settings!")
        print("⚠️  Add this URL to CSRF_TRUSTED_ORIGINS in settings.py")
        print("="*60)
        
        # Keep the script running to maintain the tunnel
        print("\n⏳ ngrok tunnel is active. Press Ctrl+C to stop...")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Shutting down ngrok tunnel...")
            ngrok.kill()
            print("✅ ngrok tunnel closed.")
            
    except Exception as e:
        print(f"❌ Error starting ngrok tunnel: {e}")
        print("💡 Make sure you have an ngrok account and have set up your authtoken")
        print("   Run: ngrok config add-authtoken YOUR_TOKEN")

if __name__ == "__main__":
    start_ngrok_tunnel()