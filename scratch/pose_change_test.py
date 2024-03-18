import numpy as np

noise_level = 0.1   # Noise level for the synthesized data

def rotation_matrix_to_euler_angles(R):
    # Ensure the matrix is in the right shape and type
    R = np.asarray(R)
    
    # Syntactic sugar for readability
    r11, r12, r13 = R[0, 0], R[0, 1], R[0, 2]
    r21, r22, r23 = R[1, 0], R[1, 1], R[1, 2]
    r31, r32, r33 = R[2, 0], R[2, 1], R[2, 2]

    # Yaw: ψ
    yaw = np.arctan2(r21, r11)
    
    # Pitch: θ
    pitch = np.arcsin(-r31)
    
    # Roll: φ
    roll = np.arctan2(r32, r33)

    # Convert from radians to degrees
    yaw_deg = np.degrees(yaw)
    pitch_deg = np.degrees(pitch)
    roll_deg = np.degrees(roll)

    return yaw_deg, pitch_deg, roll_deg

def compute_3D_transform(source_points, target_points):
    # Ensure the points are numpy arrays for matrix operations
    source_points = np.asarray(source_points)
    target_points = np.asarray(target_points)
    
    print("Noise Level:", noise_level)
    print("Source Points:\n", source_points)
    print("Target Points:\n", target_points)
    # introduce some noise to the target points
    target_points += np.random.normal(0, noise_level, target_points.shape)
    print("Target Points with noise:\n", target_points)

    # Step 1: Centering the points by computing the centroids
    centroid_source = np.mean(source_points, axis=0)
    centroid_target = np.mean(target_points, axis=0)

    # Step 2: Aligning the centroids to the origin
    source_centered = source_points - centroid_source
    target_centered = target_points - centroid_target

    # Step 3: Computing the covariance matrix
    covariance_matrix = np.dot(source_centered.T, target_centered)

    # Step 4: Applying SVD
    U, _, Vt = np.linalg.svd(covariance_matrix)

    # Step 5: Determining the rotation
    R = np.dot(Vt.T, U.T)

    # Step 6: Correcting the rotation matrix for a possible reflection
    if np.linalg.det(R) < 0:
        Vt[2, :] *= -1
        R = np.dot(Vt.T, U.T)

    # Step 7: Computing the translation
    t = centroid_target - np.dot(R, centroid_source)

    return R, t

# Testing the code with synthesized data
def test_3D_transform():
    np.random.seed(42)  # For reproducible results
    num_points = 4
    source_points = np.random.rand(num_points, 3)  # Random set of points

    # Known rotation and translation for testing
    known_rotation = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]])
    # known_rotation = np.eye(3)  # Identity matrix
    known_translation = np.array([1, 2, 3])

    # Apply known rotation and translation to synthesize target points
    target_points = np.dot(source_points, known_rotation.T) + known_translation

    # Compute the 3D pose change
    computed_rotation, computed_translation = compute_3D_transform(source_points, target_points)

    yaw, pitch, roll = rotation_matrix_to_euler_angles(computed_rotation)
    yaw_known, pitch_known, roll_known = rotation_matrix_to_euler_angles(known_rotation)

    # Apply the computed rotation and translation to the source points
    transformed_source_points = np.dot(source_points, computed_rotation.T) + computed_translation
    print("Transformed Source Points:\n", transformed_source_points)

    # Results
    # print("Computed Rotation:\n", computed_rotation)
    print("Computed Translation:\n", computed_translation)
    print(f"Compu Yaw: {yaw:.2f}°, Pitch: {pitch:.2f}°, Roll: {roll:.2f}°")
    # print("Known Rotation:\n", known_rotation)
    print("Known Translation:\n", known_translation)
    print(f"Known Yaw: {yaw_known:.2f}°, Pitch: {pitch_known:.2f}°, Roll: {roll_known:.2f}°")

    # Verify the results are close to the known transformation
    assert np.allclose(computed_rotation, known_rotation, atol=noise_level*3), "Rotation not as expected"
    assert np.allclose(computed_translation, known_translation, atol=noise_level*3), "Translation not as expected"

    return "Test passed successfully!"

# Run the test function and display the results
print(test_3D_transform())
