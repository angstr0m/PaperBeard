from unittest import TestCase
from unittest.mock import MagicMock
from paper_beard import export


class TestExport(TestCase):
    def test_csv(self):
        result_mock = MagicMock()
        result_mock.get.side_effect = ['foo', 'bar', 'baz', 'foo', 'bar', 'baz']
        results = [result_mock]
        buffer = export.csv_export(results, MagicMock())
        print(buffer.write.mock_calls)
        buffer.write.assert_any_call("title;author;year;citations;link;excerpt\r\n")
        buffer.write.assert_any_call("foo;bar;baz;foo;bar;baz\r\n")
        self.assertEqual(2, len(buffer.write.mock_calls))

    def test_bibtex(self):
        pass