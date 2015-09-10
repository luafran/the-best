import unittest

from thebest.common import exceptions


class TestExceptions(unittest.TestCase):
    def testGeneralInfoException(self):
        try:
            raise exceptions.GeneralInfoException("Testing GeneralInfoException")
        except exceptions.GeneralInfoException:
            pass

    def testBadRequest(self):
        try:
            raise exceptions.BadRequest("Testing BadRequest")
        except exceptions.BadRequest:
            pass

    def testMissingArgumentValue(self):
        try:
            raise exceptions.MissingArgumentValue("Testing MissingArgumentValue")
        except exceptions.MissingArgumentValue:
            pass

    def testInvalidArgumentValue(self):
        try:
            raise exceptions.InvalidArgumentValue("Testing InvalidArgumentValue")
        except exceptions.InvalidArgumentValue:
            pass

    def testForbidden(self):
        try:
            raise exceptions.Forbidden("Testing Forbidden")
        except exceptions.Forbidden:
            pass

    def testUnauthorized(self):
        try:
            raise exceptions.Unauthorized("Testing Unauthorized")
        except exceptions.Unauthorized:
            pass

    def testUnauthorizedRead(self):
        try:
            raise exceptions.UnauthorizedRead("Testing UnauthorizedRead")
        except exceptions.UnauthorizedRead:
            pass

    def testUnauthorizedWrite(self):
        try:
            raise exceptions.UnauthorizedWrite("Testing UnauthorizedWrite")
        except exceptions.UnauthorizedWrite:
            pass

    def testUnauthorizedExecute(self):
        try:
            raise exceptions.UnauthorizedExecute("Testing UnauthorizedExecute")
        except exceptions.UnauthorizedExecute:
            pass

    def testNotFound(self):
        try:
            raise exceptions.NotFound("Testing NotFound")
        except exceptions.NotFound:
            pass

    def testMethodNotAllowed(self):
        try:
            raise exceptions.MethodNotAllowed("Testing MethodNotAllowed")
        except exceptions.MethodNotAllowed:
            pass

    def testCouldNotConnectToDatabase(self):
        try:
            raise exceptions.CouldNotConnectToDatabase("Testing CouldNotConnectToDatabase")
        except exceptions.CouldNotConnectToDatabase:
            pass

    def testDatabaseOperationError(self):
        try:
            raise exceptions.DatabaseOperationError("Testing DatabaseOperationError")
        except exceptions.DatabaseOperationError:
            pass

    def testExternalProviderUnavailablePermanently(self):
        try:
            raise exceptions.ExternalProviderUnavailablePermanently(
                "Testing ExternalProviderUnavailablePermanently")
        except exceptions.ExternalProviderUnavailablePermanently:
            pass

    def testExternalProviderUnavailableTemporarily(self):
        try:
            raise exceptions.ExternalProviderUnavailableTemporarily(
                "Testing ExternalProviderUnavailableTemporarily")
        except exceptions.ExternalProviderUnavailableTemporarily:
            pass

    def testExternalProviderBadResponse(self):
        try:
            raise exceptions.ExternalProviderBadResponse("Testing ExternalProviderBadResponse")
        except exceptions.ExternalProviderBadResponse:
            pass
