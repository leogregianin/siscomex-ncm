import pytest
from unittest.mock import patch

from ncm.client import FetchNcm
from ncm.exceptions import NcmDownloadException


class TestNcmDownloadError:

    def test_exceptions_download_error(self):
        ncm = FetchNcm()
        with patch('ncm.client.FetchNcm.download_json', side_effect=NcmDownloadException('Error ABC')):
            with pytest.raises(NcmDownloadException) as error:
                ncm.download_json('mock:8080')
            assert str(error.value) == "Error: API not return 200 with the message Error ABC"
