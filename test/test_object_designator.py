import unittest
import test_bullet_world
from pycram.designators.object_designator import *
from pycram.enums import ObjectType


class TestObjectDesignator(test_bullet_world.BulletWorldTest):

    def test_object_grounding(self):
        description = ObjectDesignatorDescription(["milk"], [ObjectType.MILK])
        obj = description.ground()

        self.assertEqual(obj.name, "milk")
        self.assertEqual(obj.obj_type, ObjectType.MILK)

    def test_data_copy(self):
        description = ObjectDesignatorDescription(["milk"], [ObjectType.MILK])
        obj = description.ground()

        data_copy = obj.data_copy()
        self.assertEqual(obj.pose, data_copy.pose)


if __name__ == '__main__':
    unittest.main()
