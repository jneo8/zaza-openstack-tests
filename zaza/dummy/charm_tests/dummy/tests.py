"""Encapsulate dummy testing."""
import logging
import urllib3

import zaza.model as zaza_model
import zaza.openstack.charm_tests.test_utils as test_utils


class DummyTest(test_utils.BaseCharmTest):

    def setUp(self):
        """Execute this setup before each test."""
        self.tested_unit = zaza_model.get_unit_from_name(self.lead_unit)

    @classmethod
    def setUpClass(cls, application_name=None, model_alias=None):
        """Run class setup for running tests."""
        super().setUpClass(application_name="dummy", model_alias=model_alias)

    def tearDown(self):
        """Remove test resources."""
        logging.info("Running teardown")

    def test_service_alive(self):
        """Test that Apache service is listening on expected port."""
        self._check_service_alive()

    def _check_service_alive(self):
        config = zaza_model.get_application_config(self.application_name)
        port = config["port"]["value"]
        address = zaza_model.get_unit_public_address(self.tested_unit)
        test_url = "http://{}:{}/".format(address, port)

        logging.info("Testing response from apache at"
                     " {}".format(test_url))

        http = urllib3.PoolManager()
        response = http.request("GET", test_url)

        self.assertEqual(response.status, 200)

    def test_action_restart(self):
        """Test service alive after restart action."""
        zaza_model.block_until_all_units_idle(timeout=60)
        self.tested_unit.run_action(
            action_name="restart",
        )
        zaza_model.block_until_all_units_idle(timeout=60)

        self._check_service_alive()

    def test_config_change(self):
        """Test config change actually work.

        Steps:
            - Change config port.
            - Service alive on different port.
        """
        # Dict of charm settings to change to
        alternate_config = {"port": "8080"}
        default_config = {"port": "80"}

        with self.config_change(
            alternate_config=alternate_config,
            default_config=default_config,
        ):
            self._check_service_alive()
