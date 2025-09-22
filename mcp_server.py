#!/usr/bin/env python3
"""
MCP (Model Context Protocol) Server Implementation
Ein funktionierender MCP Server für OpenAI Integration
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
import sys
import os

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class MCPRequest:
    """MCP Request Structure"""
    jsonrpc: str = "2.0"
    id: Optional[str] = None
    method: str = ""
    params: Optional[Dict[str, Any]] = None

@dataclass
class MCPResponse:
    """MCP Response Structure"""
    jsonrpc: str = "2.0"
    id: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, Any]] = None

class MCPServer:
    """MCP Server Implementation"""
    
    def __init__(self):
        self.tools = {}
        self.resources = {}
        self.initialized = False
        
    async def handle_request(self, request_data: str) -> str:
        """Handle incoming MCP request"""
        try:
            request = json.loads(request_data)
            method = request.get("method")
            request_id = request.get("id")
            
            logger.info(f"Handling request: {method}")
            
            if method == "initialize":
                return await self._handle_initialize(request, request_id)
            elif method == "tools/list":
                return await self._handle_tools_list(request, request_id)
            elif method == "tools/call":
                return await self._handle_tools_call(request, request_id)
            elif method == "resources/list":
                return await self._handle_resources_list(request, request_id)
            elif method == "resources/read":
                return await self._handle_resources_read(request, request_id)
            else:
                return self._create_error_response(request_id, -32601, f"Method not found: {method}")
                
        except json.JSONDecodeError:
            return self._create_error_response(None, -32700, "Parse error")
        except Exception as e:
            logger.error(f"Error handling request: {e}")
            return self._create_error_response(request.get("id") if 'request' in locals() else None, -32603, str(e))
    
    async def _handle_initialize(self, request: Dict, request_id: str) -> str:
        """Handle initialize request"""
        self.initialized = True
        
        response = {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {},
                    "resources": {}
                },
                "serverInfo": {
                    "name": "light-autom8-mcp-server",
                    "version": "1.0.0"
                }
            }
        }
        
        return json.dumps(response)
    
    async def _handle_tools_list(self, request: Dict, request_id: str) -> str:
        """Handle tools/list request"""
        tools = [
            {
                "name": "create_vector_store",
                "description": "Erstellt einen neuen Vector Store für OpenAI",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Name des Vector Stores"
                        }
                    },
                    "required": ["name"]
                }
            },
            {
                "name": "upload_file_to_vector_store",
                "description": "Lädt eine Datei in einen Vector Store hoch",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "vector_store_id": {
                            "type": "string",
                            "description": "ID des Vector Stores"
                        },
                        "file_content": {
                            "type": "string",
                            "description": "Inhalt der Datei"
                        },
                        "file_name": {
                            "type": "string",
                            "description": "Name der Datei"
                        }
                    },
                    "required": ["vector_store_id", "file_content"]
                }
            },
            {
                "name": "list_vector_stores",
                "description": "Listet alle verfügbaren Vector Stores auf",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            }
        ]
        
        response = {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "tools": tools
            }
        }
        
        return json.dumps(response)
    
    async def _handle_tools_call(self, request: Dict, request_id: str) -> str:
        """Handle tools/call request"""
        params = request.get("params", {})
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        try:
            if tool_name == "create_vector_store":
                result = await self._create_vector_store(arguments)
            elif tool_name == "upload_file_to_vector_store":
                result = await self._upload_file_to_vector_store(arguments)
            elif tool_name == "list_vector_stores":
                result = await self._list_vector_stores(arguments)
            else:
                raise ValueError(f"Unknown tool: {tool_name}")
            
            response = {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(result, indent=2)
                        }
                    ]
                }
            }
            
        except Exception as e:
            response = {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32603,
                    "message": str(e)
                }
            }
        
        return json.dumps(response)
    
    async def _handle_resources_list(self, request: Dict, request_id: str) -> str:
        """Handle resources/list request"""
        resources = [
            {
                "uri": "file://customer_policies.txt",
                "name": "Customer Policies",
                "description": "Kundenrichtlinien und FAQ-Dokument",
                "mimeType": "text/plain"
            }
        ]
        
        response = {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "resources": resources
            }
        }
        
        return json.dumps(response)
    
    async def _handle_resources_read(self, request: Dict, request_id: str) -> str:
        """Handle resources/read request"""
        params = request.get("params", {})
        uri = params.get("uri")
        
        try:
            if uri == "file://customer_policies.txt":
                with open("customer_policies.txt", "r", encoding="utf-8") as f:
                    content = f.read()
            else:
                raise ValueError(f"Unknown resource: {uri}")
            
            response = {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "contents": [
                        {
                            "uri": uri,
                            "mimeType": "text/plain",
                            "text": content
                        }
                    ]
                }
            }
            
        except Exception as e:
            response = {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32603,
                    "message": str(e)
                }
            }
        
        return json.dumps(response)
    
    async def _create_vector_store(self, arguments: Dict) -> Dict:
        """Create a new vector store"""
        # Hier würde die OpenAI API Integration stattfinden
        name = arguments.get("name", "Default Vector Store")
        
        return {
            "success": True,
            "vector_store_id": f"vs_{hash(name)}",
            "name": name,
            "status": "ready"
        }
    
    async def _upload_file_to_vector_store(self, arguments: Dict) -> Dict:
        """Upload file to vector store"""
        vector_store_id = arguments.get("vector_store_id")
        file_content = arguments.get("file_content")
        file_name = arguments.get("file_name", "uploaded_file.txt")
        
        return {
            "success": True,
            "file_id": f"file_{hash(file_content)}",
            "vector_store_id": vector_store_id,
            "file_name": file_name,
            "status": "uploaded"
        }
    
    async def _list_vector_stores(self, arguments: Dict) -> Dict:
        """List all vector stores"""
        return {
            "success": True,
            "vector_stores": [
                {
                    "id": "vs_1",
                    "name": "Support FAQ",
                    "status": "ready",
                    "created_at": "2024-09-22T23:20:00Z"
                }
            ]
        }
    
    def _create_error_response(self, request_id: Optional[str], code: int, message: str) -> str:
        """Create error response"""
        response = {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": code,
                "message": message
            }
        }
        return json.dumps(response)

async def main():
    """Main function to run the MCP server"""
    server = MCPServer()
    
    logger.info("MCP Server starting...")
    logger.info("Listening for JSON-RPC requests on stdin")
    
    try:
        while True:
            # Read from stdin
            line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
            if not line:
                break
            
            line = line.strip()
            if not line:
                continue
            
            # Handle the request
            response = await server.handle_request(line)
            print(response, flush=True)
            
    except KeyboardInterrupt:
        logger.info("MCP Server shutting down...")
    except Exception as e:
        logger.error(f"Server error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
