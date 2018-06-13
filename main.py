import sys
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--port", dest="port",
                        required=False,
                        type=int,
                        default=8000,
                        help="""The port server listen on. Default is 8000.""")
    parser.add_argument("--host", dest="host",
                        required=False,
                        default="localhost",
                        help="""The address server bind to. Default is localhost.""")
    parser.add_argument("--debug", dest="debug",
                        required=False,
                        action="store_true",
                        default=False,
                        help="""The server run on debug mode or not.""")
    parser.add_argument("--server-type", dest="server_type",
                        required=False,
                        default="flask",
                        help="type of server. It can be 'flask' or 'broker'")
    argv = parser.parse_args(sys.argv[1:])
    server_type = argv.server_type
    host = argv.host
    port = argv.port
    debug = argv.debug

    if server_type.lower() == "explorer":
        import explorer
        explorer.application.run(host=host, port=port, debug=debug)
