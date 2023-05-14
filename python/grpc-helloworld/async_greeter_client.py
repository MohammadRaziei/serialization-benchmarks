# Copyright 2020 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python AsyncIO implementation of the GRPC helloworld.Greeter client."""

import asyncio
import logging
import faker
import numpy as np

import grpc
from myproto import helloworld_pb2_grpc
from myproto.helloworld_pb2 import HelloRequest, HelloReply

from google.protobuf import json_format
import ujson

fake = faker.Faker()




async def run() -> None:
    
    requestDict = {
                "name": fake.name(), "query": fake.sentence(), 
                "features": [dict(address=fake.address(), 
                                    vec=np.random.randn(256).tolist())
                            for _ in range(2000)]
                }
    
    request_obj = HelloRequest();
    json_format.ParseDict(requestDict, request_obj)

    # features = [HelloRequest.Features(address=fake.address(), 
    #                                   vec=np.random.randint(0, 256, 2))
    #             for _ in range(2)]
    # request_obj = HelloRequest(name=fake.name(), query=fake.sentence(), features=features)
        
    async with grpc.aio.insecure_channel('localhost:50051') as channel:
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        response = await stub.SayHello(request_obj)

    requestJsonBytes = ujson.dumps(requestDict).encode("utf-8")
    requestJsonBytesLen = len(requestJsonBytes)
    print("Bytes:", requestJsonBytesLen, request_obj.ByteSize(), request_obj.ByteSize() / requestJsonBytesLen)
    print("Greeter client received: " + response.name)


if __name__ == '__main__':
    logging.basicConfig()
    asyncio.run(run())
