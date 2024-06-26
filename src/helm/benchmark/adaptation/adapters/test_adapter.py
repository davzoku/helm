import shutil
import tempfile

from helm.benchmark.config_registry import register_builtin_configs_from_helm_package
from helm.common.authentication import Authentication
from helm.proxy.services.server_service import ServerService
from helm.benchmark.window_services.tokenizer_service import TokenizerService


class TestAdapter:
    """
    Has setup and teardown methods downstream Adapter tests need.
    """

    def setup_method(self):
        register_builtin_configs_from_helm_package()
        self.path: str = tempfile.mkdtemp()
        service = ServerService(base_path=self.path, root_mode=True)
        self.tokenizer_service = TokenizerService(service, Authentication("test"))

    def teardown_method(self, _):
        shutil.rmtree(self.path)
