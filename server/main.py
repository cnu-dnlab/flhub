FLAGS = _ = None
DEBUG = False


def main():
    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=10))
    federated_pb2_grpc.add_ManagerServicer_to_server(Server(), server)
    server.add_insecure_port(f'{FLAGS.address}:{FLAGS.port}')
    server.start()
    if DEBUG:
        print(f'[{int(time.time()-STIME)}] Start server')
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        server.wait_for_termination(1)
    if DEBUG:
        print(f'[{int(time.time()-STIME)}] End server')


if __name__ == '__main__':
    root_path = os.path.abspath(__file__)
    root_dir = os.path.dirname(root_path)
    os.chdir(root_dir)

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true',
                        help='The present debug message')
    parser.add_argument('--address', type=str, default='[::]',
                        help='The bind address')
    parser.add_argument('--port', type=int, default=50000,
                        help='The bind port number')

    FLAGS, _ = parser.parse_known_args()
    DEBUG = FLAGS.debug

    main()

