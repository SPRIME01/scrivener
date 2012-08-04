from twisted.application.service import ServiceMaker

scribe = ServiceMaker(
        "A scribe server",
        "scrivener.tap",
        "The thrift scribe service.s",
        "scrivener")
