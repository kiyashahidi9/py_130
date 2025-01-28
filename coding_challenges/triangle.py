'''
input: A triangle object with 3 sides
output: a triangle.kind attribute determination

rules:
    - equilateral triangle: all 3 sides are exactly the same length
    - isosceles triangle: only 2 sides have exactly the same length
    - scalene triangle: all sides have different lengths

    - to be a triangle:
        - all sides must have a length > 0
        - the sum of the lengths of any two sides must be greater
        than the length of the third side

data/object structure:

Triangle
    - init
        - self.side1
        - self.side2
        - self.side3
    - is_triangle (behavior)
    - kind (property)
    
ALG:
1. instantiate a triangle object, initialize the length of the 3 sides
2. check if the object is a valid triangle
3. determine the kind of the triangle

step 2: is_triangle
1. iterate through a list of the sides
2. if any side is <= 0, is_triangle is False
3. if side1 + side2 < side3
    - side1 + side3 < side2
    - side2 + side3 < side1
    - is_triangle is False

step 3: determine the kind
1. if side1 == side2 == side3
    - self.kind is equilateral
2. if side1 != side2 != side3
    - self.kind is scalene
3. if (side1 == side2) and side1 != side3
    - or (side1 == side3) and side1 != side2
    - or (side2 == side3) and side2 != side1
    - self.kind is isosceles
'''

class Triangle:
    def __init__(self, side1, side2, side3):
        self.side1 = side1
        self.side2 = side2
        self.side3 = side3
        self.is_triangle()
        self.kind = self.determine_kind()
    
    def is_triangle(self):
        for side in [self.side1, self.side2, self.side3]:
            if side <= 0:
                raise ValueError()

        side1, side2, side3 = self.side1, self.side2, self.side3

        if ((side1 + side2 <= side3) or
            (side1 + side3 <= side2) or
            (side2 + side3 <= side1)):

            raise ValueError()

    def determine_kind(self):
        side1, side2, side3 = self.side1, self.side2, self.side3
        
        if side1 == side2 == side3:
            return 'equilateral'
        elif side1 != side2 != side3 != side1:
            return 'scalene'
        elif ((side1 == side2) and (side1 != side3) or 
            (side1 == side3) and (side1 != side2) or 
            (side2 == side3) and (side2 != side1)):
            return 'isosceles'
