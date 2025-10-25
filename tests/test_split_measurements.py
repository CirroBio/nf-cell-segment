import unittest
from pathlib import Path

from bin.split_measurements import parse_stardist


test_data_path = Path(__file__).parent / "data"


class TestSplitMeasurements(unittest.TestCase):
    def test_parse_stardist(self):
        partition, spatial, attributes = parse_stardist(test_data_path / 'measurements.csv')

        self.assertTrue('Cell.Mean' in partition)
        self.assertTrue('Cell.Std.Dev.' in partition)
        self.assertTrue('Nucleus.Mean' in partition)
        self.assertEqual(len(partition['Cell.Mean'].columns), 16)
        self.assertEqual(spatial.shape, (1, 2))
        self.assertEqual(attributes.shape, (1, 15))


if __name__ == '__main__':
    unittest.main()
