from twisted.application.service import ServiceMaker

scribe = ServiceMaker(
        "A scribe server",
        "txScribe.tap",
        "The thrift scribe service.s",
        "scribe")
