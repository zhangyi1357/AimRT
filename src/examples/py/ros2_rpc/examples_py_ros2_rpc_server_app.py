# Copyright (c) 2024 The AimRT Authors.
# AimRT is licensed under Mulan PSL v2.

import argparse
import signal
import sys
import threading

import aimrt_py
import example_ros2.srv
import rpc_code

global_aimrt_core = None


def signal_handler(sig, frame):
    global global_aimrt_core

    if (global_aimrt_core and (sig == signal.SIGINT or sig == signal.SIGTERM)):
        global_aimrt_core.Shutdown()
        return

    sys.exit(0)


class ExampleServiceImpl(rpc_code.ExampleRos2Service):
    def __init__(self, logger):
        super().__init__()
        self.logger = logger

    @staticmethod
    def PrintMetaInfo(logger, ctx_ref):
        meta_keys = ctx_ref.GetMetaKeys()
        for key in meta_keys:
            aimrt_py.info(logger, f"meta key: {key}, value: {ctx_ref.GetMetaValue(key)}")

    def RosTestRpc(self, ctx_ref, req):
        rsp = example_ros2.srv.RosTestRpc.Response()
        rsp.code = 1000
        rsp.string_data = "Hello, AimRT!"
        rsp.wstring_data = "Hello, AimRT!1111111111111111"
        rsp.bool_data = True
        rsp.byte_data = bytes([1])
        rsp.char_data = 92
        rsp.float32_data = float(1.1)
        rsp.float64_data = float(2.2)
        rsp.int8_data = int(-8)
        rsp.uint8_data = int(8)
        rsp.int16_data = int(-16)
        rsp.uint16_data = int(16)
        rsp.int32_data = int(-32)
        rsp.uint32_data = int(32)
        rsp.int64_data = int(-64)
        rsp.uint64_data = int(64)

        ExampleServiceImpl.PrintMetaInfo(self.logger, ctx_ref)
        aimrt_py.info(self.logger,
                      f"Server handle new rpc call. "
                      f"context: {ctx_ref.ToString()}, "
                      f"req: {req}, "
                      f"return rsp: {rsp}")

        return aimrt_py.RpcStatus(), rsp


def main():
    parser = argparse.ArgumentParser(description='Example rpc server app.')
    parser.add_argument('--cfg_file_path', type=str, default="", help='config file path')
    args = parser.parse_args()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    print("AimRT start.")

    aimrt_core = aimrt_py.Core()

    global global_aimrt_core
    global_aimrt_core = aimrt_core

    # Initialize
    core_options = aimrt_py.CoreOptions()
    core_options.cfg_file_path = args.cfg_file_path
    aimrt_core.Initialize(core_options)

    # Create Module
    module_handle = aimrt_core.CreateModule("NormalRpcServerPyModule")

    # Register rpc service
    service = ExampleServiceImpl(module_handle.GetLogger())
    ret = module_handle.GetRpcHandle().RegisterService(service)
    assert ret, "Register service failed."

    # Start
    thread = threading.Thread(target=aimrt_core.Start)
    thread.start()

    while thread.is_alive():
        thread.join(1.0)

    print("AimRT exit.")


if __name__ == '__main__':
    main()
