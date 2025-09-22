#!/usr/bin/env python3
"""
Test Script für MCP Server
Testet die verschiedenen MCP Funktionen
"""

import asyncio
import json
import subprocess
import sys
import time

class MCPTester:
    def __init__(self):
        self.server_process = None
    
    async def start_server(self):
        """Starte den MCP Server"""
        print("🚀 Starte MCP Server...")
        self.server_process = subprocess.Popen(
            [sys.executable, "mcp_server.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        await asyncio.sleep(1)  # Warte kurz bis Server startet
        print("✅ MCP Server gestartet")
    
    async def send_request(self, request: dict) -> dict:
        """Sende eine Anfrage an den MCP Server"""
        request_json = json.dumps(request) + "\n"
        self.server_process.stdin.write(request_json)
        self.server_process.stdin.flush()
        
        # Lese Antwort
        response_line = self.server_process.stdout.readline()
        return json.loads(response_line.strip())
    
    async def test_initialize(self):
        """Teste die Initialize-Funktion"""
        print("\n🔧 Teste Initialize...")
        request = {
            "jsonrpc": "2.0",
            "id": "1",
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }
        
        response = await self.send_request(request)
        print(f"✅ Initialize Response: {json.dumps(response, indent=2)}")
        return response
    
    async def test_tools_list(self):
        """Teste die Tools-Liste"""
        print("\n🛠️ Teste Tools List...")
        request = {
            "jsonrpc": "2.0",
            "id": "2",
            "method": "tools/list"
        }
        
        response = await self.send_request(request)
        print(f"✅ Tools List Response: {json.dumps(response, indent=2)}")
        return response
    
    async def test_tool_call(self):
        """Teste einen Tool-Aufruf"""
        print("\n🔨 Teste Tool Call...")
        request = {
            "jsonrpc": "2.0",
            "id": "3",
            "method": "tools/call",
            "params": {
                "name": "create_vector_store",
                "arguments": {
                    "name": "Test Vector Store"
                }
            }
        }
        
        response = await self.send_request(request)
        print(f"✅ Tool Call Response: {json.dumps(response, indent=2)}")
        return response
    
    async def test_resources_list(self):
        """Teste die Resources-Liste"""
        print("\n📚 Teste Resources List...")
        request = {
            "jsonrpc": "2.0",
            "id": "4",
            "method": "resources/list"
        }
        
        response = await self.send_request(request)
        print(f"✅ Resources List Response: {json.dumps(response, indent=2)}")
        return response
    
    async def test_resources_read(self):
        """Teste das Lesen einer Resource"""
        print("\n📖 Teste Resources Read...")
        request = {
            "jsonrpc": "2.0",
            "id": "5",
            "method": "resources/read",
            "params": {
                "uri": "file://customer_policies.txt"
            }
        }
        
        response = await self.send_request(request)
        print(f"✅ Resources Read Response: {json.dumps(response, indent=2)}")
        return response
    
    async def run_all_tests(self):
        """Führe alle Tests aus"""
        try:
            await self.start_server()
            
            # Führe alle Tests aus
            await self.test_initialize()
            await self.test_tools_list()
            await self.test_tool_call()
            await self.test_resources_list()
            await self.test_resources_read()
            
            print("\n🎉 Alle Tests erfolgreich abgeschlossen!")
            
        except Exception as e:
            print(f"❌ Test Fehler: {e}")
        finally:
            if self.server_process:
                self.server_process.terminate()
                print("🛑 MCP Server gestoppt")

async def main():
    tester = MCPTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())
