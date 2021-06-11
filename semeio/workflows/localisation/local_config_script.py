# Localisation configuration script
# Written by: O.Lia
# Date: Mayl 2021
# Current version:
#   Localisation configuration file in YAML format is read for
#   parameters and this script setup the localisation in ERT.

from ert_shared.plugins.plugin_manager import hook_implementation
from res.enkf.enums.ert_impl_type_enum import ErtImplType

from semeio.communication import SemeioScript
import semeio.workflows.localisation.local_script_lib as local
from semeio.workflows.localisation.local_config_script import LocalisationConfig


debug_level = 1


class LocalisationConfigJob(SemeioScript):
    def run(self, *args):
        ert = self.ert()

        # Clear all correlations
        local.clear_correlations(ert)

        # Read yml file with specifications
        all_kw = local.read_localisation_config(args)

        # Get all observations from ert instance
        ert_obs_list = local.get_observations_from_ert(ert)
        if debug_level > 0:
            print(" -- Node names for observations found in ERT configuration:")
            for obs_name in ert_obs_list:
                print(f"      {obs_name}")
            print("\n")

        # Get all parameters nodes with parameters defined by GEN_KW from ert instance
        ert_param_dict = local.get_param_from_ert(ert, impl_type=ErtImplType.GEN_KW)
        if debug_level > 0:
            print(
                f"-- All specified scalar parameters from ERT instance:\n"
                f"{ert_param_dict}\n"
            )

        conf = LocalisationConfig(
            observations=ert_obs_list, parameters=ert_param_dict, **all_kw
        )

        local.add_ministeps(conf.correlations, ert_param_dict, ert)


@hook_implementation
def legacy_ertscript_workflow(config):
    workflow = config.add_workflow(LocalisationConfigJob, "LOCALISATION_JOB")
    workflow.description = "test"
    workflow.category = "observations.correlation"