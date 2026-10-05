"""
Activity 3: 3D Computational Geometry & Spatial Collision Engine
"""

import math
import random
import time

"""
1. 3D GEOMETRIC VECTOR MATH ENGINE
"""
class Vector3D:
    """3D Vector representation with core spatial linear algebra operations."""
    def __init__(self, x: float, y: float, z: float):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __repr__(self):
        return f"Vector3D({self.x:.2f}, {self.y:.2f}, {self.z:.2f})"

    def __sub__(self, other: 'Vector3D') -> 'Vector3D':
        """Vector Subtraction: V_sub = V1 - V2"""
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def __add__(self, other: 'Vector3D') -> 'Vector3D':
        """Vector Addition: V_add = V1 + V2"""
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def dot(self, other: 'Vector3D') -> float:
        """Dot Product: V1 . V2 = x1*x2 + y1*y2 + z1*z2"""
        return self.x * other.x + self.y * other.y + self.z * other.z

    def magnitude_squared(self) -> float:
        """Calculates squared length (avoids square root overhead)."""
        return self.x**2 + self.y**2 + self.z**2

    def magnitude(self) -> float:
        """Euclidean Length: ||V|| = sqrt(x^2 + y^2 + z^2)"""
        return math.sqrt(self.magnitude_squared())

    def distance_to(self, other: 'Vector3D') -> float:
        """3D Euclidean Distance: d = ||P1 - P2||"""
        return (self - other).magnitude()

    def get_octant(self) -> int:
        """
        Determines the 3D Octant (1 through 8) based on signs of (x, y, z):
        Octant 1: (+,+,+) | Octant 2: (-,+,+) | Octant 3: (-,-,+) | Octant 4: (+,-,+)
        Octant 5: (+,+,-) | Octant 6: (-,+,-) | Octant 7: (-,-,-) | Octant 8: (+,-,-)
        """
        x_pos = self.x >= 0
        y_pos = self.y >= 0
        z_pos = self.z >= 0

        if z_pos:
            if x_pos and y_pos: return 1
            if not x_pos and y_pos: return 2
            if not x_pos and not y_pos: return 3
            if x_pos and not y_pos: return 4
        else:
            if x_pos and y_pos: return 5
            if not x_pos and y_pos: return 6
            if not x_pos and not y_pos: return 7
            if x_pos and not y_pos: return 8


"""
2. SLIDE VERIFICATION PROBLEM SETS
"""
def run_slide_verifications():
    print("=" * 65)
    print(" 1. SLIDE VERIFICATION PROBLEM SETS")
    print("=" * 65)

    """
    Example 3 Verification
    Given Points: P1(1, 2, 3) and P2(3, 0, 2)
    Expected Distance: sqrt((3-1)^2 + (0-2)^2 + (2-3)^2) = sqrt(4 + 4 + 1) = sqrt(9) = 3
    """
    p1 = Vector3D(1, 2, 3)
    p2 = Vector3D(3, 0, 2)
    calc_dist = p1.distance_to(p2)

    print("\n[Example 3 Verification]")
    print(f"Point 1: {p1} | Point 2: {p2}")
    print(f"Calculated Distance: {calc_dist:.4f}")
    print(f"Status: {'PASSED (Distance = 3.0)' if math.isclose(calc_dist, 3.0) else 'FAILED'}")

    """
    Example 5 Verification
    Given Sphere Equation: x^2 + y^2 + z^2 - 4x + 6y - 8z + 4 = 0
    Complete the Squares:
    (x - 2)^2 - 4 + (y + 3)^2 - 9 + (z - 4)^2 - 16 + 4 = 0
    (x - 2)^2 + (y + 3)^2 + (z - 4)^2 = 25
    Expected Center: (2, -3, 4), Expected Radius: sqrt(25) = 5
    """
    coeff_x, coeff_y, coeff_z, const_term = -4.0, 6.0, -8.0, 4.0

    """Completing square algebraically: (x + coeff/2)^2 => Center = -coeff/2"""
    center_x = -coeff_x / 2.0
    center_y = -coeff_y / 2.0
    center_z = -coeff_z / 2.0
    center = Vector3D(center_x, center_y, center_z)

    radius_sq = (center_x**2 + center_y**2 + center_z**2) - const_term
    radius = math.sqrt(radius_sq)

    print("\n[Example 5 Verification]")
    print(f"Sphere Equation: x^2 + y^2 + z^2 - 4x + 6y - 8z + 4 = 0")
    print(f"Extracted Center: {center} | Octant: {center.get_octant()}")
    print(f"Extracted Radius: {radius:.4f}")

    expected_center = Vector3D(2, -3, 4)
    expected_radius = 5.0
    passed_center = math.isclose(center.distance_to(expected_center), 0.0)
    passed_radius = math.isclose(radius, expected_radius)

    print(f"Status: {'PASSED (Center=(2, -3, 4), Radius=5.0)' if passed_center and passed_radius else 'FAILED'}")


"""
3. BOUNDING VOLUME IMPLEMENTATIONS
"""
class BoundingSphere:
    """Bounding Sphere defined by center point and radius."""
    def __init__(self, center: Vector3D, radius: float):
        self.center = center
        self.radius = float(radius)

    def intersects(self, other: 'BoundingSphere') -> bool:
        """
        Sphere-Sphere Intersection Test:
        Intersects if ||C1 - C2||^2 <= (r1 + r2)^2
        (Uses squared distance to avoid square root computation).
        """
        dist_sq = (self.center - other.center).magnitude_squared()
        radius_sum_sq = (self.radius + other.radius) ** 2
        return dist_sq <= radius_sum_sq


class AABB:
    """3D Axis-Aligned Bounding Box defined by Min and Max Extents."""
    def __init__(self, min_pt: Vector3D, max_pt: Vector3D):
        self.min = min_pt
        self.max = max_pt

    def intersects(self, other: 'AABB') -> bool:
        """
        AABB-AABB Intersection Test (Separating Axis Theorem):
        Boxes overlap if and only if they overlap on all three coordinate axes.
        """
        return (
            (self.min.x <= other.max.x and self.max.x >= other.min.x) and
            (self.min.y <= other.max.y and self.max.y >= other.min.y) and
            (self.min.z <= other.max.z and self.max.z >= other.min.z)
        )


def verify_bounding_volumes():
    print("\n" + "=" * 65)
    print(" 2. BOUNDING VOLUME INTERSECTION TESTS")
    print("=" * 65)

    """Sphere Tests"""
    s1 = BoundingSphere(Vector3D(0, 0, 0), 5.0)

    """Overlaps (dist=6 <= 5+2=7)"""
    s2 = BoundingSphere(Vector3D(6, 0, 0), 2.0)

    """Disjoint (dist=10 > 5+2=7)"""
    s3 = BoundingSphere(Vector3D(10, 0, 0), 2.0)

    print(f"Sphere 1 vs Sphere 2 (Overlapping): {s1.intersects(s2)}")
    print(f"Sphere 1 vs Sphere 3 (Disjoint):    {s1.intersects(s3)}")

    """AABB Tests"""
    box1 = AABB(Vector3D(0, 0, 0), Vector3D(5, 5, 5))

    """Overlaps box1"""
    box2 = AABB(Vector3D(3, 3, 3), Vector3D(8, 8, 8))

    """Disjoint from box1"""
    box3 = AABB(Vector3D(6, 6, 6), Vector3D(10, 10, 10))

    print(f"AABB 1 vs AABB 2 (Overlapping):     {box1.intersects(box2)}")
    print(f"AABB 1 vs AABB 3 (Disjoint):        {box1.intersects(box3)}")


"""
4. SPATIAL BROAD-PHASE COLLISION STRESS TEST
"""
def run_broad_phase_stress_test(num_objects: int = 500):
    print("\n" + "=" * 65)
    print(f" 3. SPATIAL BROAD-PHASE STRESS TEST ({num_objects} OBJECTS)")
    print("=" * 65)

    """Deterministic test run"""
    random.seed(42)

    """Generate Random Spheres"""
    spheres = []
    for _ in range(num_objects):
        c = Vector3D(random.uniform(-100, 100), random.uniform(-100, 100), random.uniform(-100, 100))
        r = random.uniform(1.0, 5.0)
        spheres.append(BoundingSphere(c, r))

    """Generate Random AABBs"""
    aabbs = []
    for _ in range(num_objects):
        c = Vector3D(random.uniform(-100, 100), random.uniform(-100, 100), random.uniform(-100, 100))
        size = Vector3D(random.uniform(1, 5), random.uniform(1, 5), random.uniform(1, 5))
        min_p = c - size
        max_p = c + size
        aabbs.append(AABB(min_p, max_p))

    """Broad-Phase Sweep for Spheres"""
    start_time = time.time()
    sphere_collisions = 0
    for i in range(num_objects):
        for j in range(i + 1, num_objects):
            if spheres[i].intersects(spheres[j]):
                sphere_collisions += 1
    sphere_time = (time.time() - start_time) * 1000.0

    """Broad-Phase Sweep for AABBs"""
    start_time = time.time()
    aabb_collisions = 0
    for i in range(num_objects):
        for j in range(i + 1, num_objects):
            if aabbs[i].intersects(aabbs[j]):
                aabb_collisions += 1
    aabb_time = (time.time() - start_time) * 1000.0

    total_checks = (num_objects * (num_objects - 1)) // 2

    print(f"Total Pairwise Evaluations: {total_checks:,}")
    print(f"Sphere Engine: {sphere_collisions} collisions detected in {sphere_time:.2f} ms")
    print(f"AABB Engine:   {aabb_collisions} collisions detected in {aabb_time:.2f} ms")


"""
MAIN EXECUTION ENTRY POINT
"""
if __name__ == "__main__":
    run_slide_verifications()
    verify_bounding_volumes()
    run_broad_phase_stress_test(num_objects=500)
