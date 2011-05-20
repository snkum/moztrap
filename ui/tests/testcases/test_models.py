from mock import patch

from ..responses import response
from ..utils import (
    BaseResourceTest, ResourceTestCase, locmem_cache)
from .builders import testcases, testcaseversions



@patch("tcmui.core.api.userAgent", spec=["request"])
class TestCaseTest(BaseResourceTest, ResourceTestCase):
    def get_resource_class(self):
        from tcmui.testcases.models import TestCase
        return TestCase


    def get_resource_list_class(self):
        from tcmui.testcases.models import TestCaseList
        return TestCaseList


    @property
    def version_class(self):
        from tcmui.testcases.models import TestCaseVersion
        return TestCaseVersion


    @property
    def version_list_class(self):
        from tcmui.testcases.models import TestCaseVersionList
        return TestCaseVersionList


    def test_post_to_testcaselist_invalidates_testcaseversionlist(self, http):
        new = self.resource_class()
        new.update_from_dict(testcases.one())

        http.request.return_value = response(testcaseversions.searchresult())

        with locmem_cache():
            tcl = self.version_list_class.get(auth=self.auth)
            tcl.deliver()

            # the API responds to posted testcases with a testcase version
            http.request.return_value = response(testcaseversions.one())

            self.resource_list_class.get(auth=self.auth).post(new)

            http.request.return_value = response(
                testcaseversions.searchresult({}))

            tcl2 = self.version_list_class.get(auth=self.auth)
            tcl2.deliver()

        self.assertEqual(len(tcl), 0)
        self.assertEqual(len(tcl2), 1)


    def test_put_to_testcase_invalidates_testcaseversion(self, http):
        http.request.return_value = response(testcases.one(name="A Test Case"))

        case = self.resource_class.get("testcases/1", auth=self.auth)
        case.deliver()

        http.request.return_value = response(
            testcaseversions.one(name="A Test Case"))

        with locmem_cache():
            v = self.version_class.get("testcases/versions/1", auth=self.auth)
            v.deliver()

            case.name = "New Name"
            case.put()

            http.request.return_value = response(
                testcaseversions.one(name="New Name"))

            v2 = self.version_class.get("testcases/versions/1", auth=self.auth)
            v2.deliver()

        self.assertEqual(v2.name, "New Name")


    def test_put_to_testcase_invalidates_testcaseversionlist(self, http):
        http.request.return_value = response(testcases.one(name="A Test Case"))

        case = self.resource_class.get("testcases/1", auth=self.auth)

        http.request.return_value = response(
            testcaseversions.searchresult({"name": "A Test Case"}))

        with locmem_cache():
            vl = self.version_list_class.get(auth=self.auth)
            vl.deliver()

            case.name = "New Name"
            case.put()

            http.request.return_value = response(
                testcaseversions.searchresult({"name": "New Name"}))

            vl2 = self.version_list_class.get(auth=self.auth)
            vl2.deliver()

        self.assertEqual(vl2[0].name, "New Name")
