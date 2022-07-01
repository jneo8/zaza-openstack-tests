"""Encapsulate dummy testing."""
import logging
import zaza.openstack.charm_tests.test_utils as test_utils


class DummyTest(test_utils.BaseCharmTest):

    @classmethod
    def setUpClass(cls):
        """Run class setup for running tests."""
        super().setUpClass(application_name="dummy")

    @classmethod
    def tearDown(cls):
        """Remove test resources."""
        logging.info("Running teardown")


    def test_dummy(self):
        """Test real doing nothing."""
        logging.info("Test dummy")

