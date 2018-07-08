from __future__ import division, absolute_import
from twisted.python import log
from twisted.internet.protocol import DatagramProtocol
from cowrie.shell.customparser import CustomParser, OptionNotFound
from cowrie.shell.honeypot import HoneyPotCommand
from twisted.application import service
from twisted.internet import reactor
import struct


commands = {}



class TftpDatagramProtocol(DatagramProtocol):

    OP_RRQ = 1
    OP_WRQ = 2
    OP_DATA = 3
    OP_ACK = 4
    OP_ERROR = 5
    OP_OACK = 6

    def __init__(self,hostname,port,filename,protocol):
        self.hostname = hostname
        self.port = port
        self.filename = filename
        self.tftpself = protocol

    def startService(self,portToListen):
        reactor.listenUDP(0,TftpDatagramProtocol)

    def startProtocol(self,filename):
        self.transport.connect(self.hostname, self.port)
        self.transport.write(struct.pack(b"!H", self.OP_RRQ,self.filename))

    def sendDatagram(self,string):
            datagram = string
            self.transport.write(datagram)

    def datagramReceived(self, datagram, host):
        self.tftpself.out.write('Datagram received: ', repr(datagram))


class command_tftp(HoneyPotCommand):
    """
    """

    port = 69
    hostname = None
    file_to_get = None

    def run(self, application,IP):

        self.tftpClient = TftpDatagramProtocol(IP,self.port, self.file,self)
        self.tftpClient.setServiceParent(application)
        self.tftpClient.startService()

    def gotIP(self):
        application = service.Application('tftp')
        self.run(application,IP)

    def start(self):
        """
        """
        parser = CustomParser(self)
        parser.prog = "tftp"
        parser.add_argument("hostname", nargs='?', default=None)
        parser.add_argument("-c", nargs=2)
        parser.add_argument("-l")
        parser.add_argument("-g")
        parser.add_argument("-p")
        parser.add_argument("-r")

        try:
            args = parser.parse_args(self.args)
            if args.c:
                if len(args.c) > 1:
                    command = args.c[0]
                    self.file_to_get = args.c[1]
                    if args.hostname is None:
                        raise OptionNotFound("Hostname is invalid")
                    self.hostname = args.hostname

            elif args.r:
                self.file_to_get = args.r
                self.hostname = args.g
            else:
                parser.print_usage()
                raise OptionNotFound("Missing!!")

            if self.hostname is None:
                raise OptionNotFound("Hostname is invalid")

            if self.hostname.find(':') != -1:
                host, port = self.hostname.split(':')
                self.hostname = host
                self.port = int(port)

            self.ip = reactor.resolve(self.hostname).addCallback(self.gotIP)


        except Exception as err:
            log.err(str(err))

        self.exit()


commands['tftp'] = command_tftp
commands['/usr/bin/tftp'] = command_tftp
