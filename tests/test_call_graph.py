# project : IPRO Revisi Header Laporan Trading Term
import unittest

from mapping.extract_db_usage import extract_data_layer_calls


class CallGraphTests(unittest.TestCase):
    def test_calls_inside_comments_and_strings_are_not_resolved(self):
        source = '''
        // Repository.Commented();
        var message = "Repository.InString()";
        Repository.Real();
        '''

        calls = extract_data_layer_calls(source, {"Repository": {"repo.cs"}})

        self.assertEqual(calls, {("Repository", "Real")})


if __name__ == "__main__":
    unittest.main()
# end project : IPRO Revisi Header Laporan Trading Term
