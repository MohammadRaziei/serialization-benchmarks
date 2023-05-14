## How to compile

```
python -m grpc_tools.protoc -I. --python_out=myproto --pyi_out=myproto --grpc_python_out=myproto helloworld.proto
```

