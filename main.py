import bpy
import os

WORKDIR = "c:\\Users\\Rodion Smilovskyi\\projects\\blender-image-generator"

object_name = "apple_basic"
source_filepath = os.path.join(WORKDIR, "models", "appleblend.blend")
output_filepath = os.path.join(WORKDIR, "output", "scene.blend")

# Append the collection
bpy.ops.wm.append(
    filepath=f"{source_filepath}\\Object\\{object_name}",
    directory=f"{source_filepath}\\Object\\",
    filename=object_name,
    link=False  # Set to True if you want to link instead of append
)


obj = bpy.data.objects.get(object_name)
if obj:
    # Set the X, Y, Z location of the object
    obj.location.x = 5.0
    obj.location.y = 2.0
    obj.location.z = 3.0

bpy.ops.wm.save_as_mainfile(filepath=output_filepath)
print(f"Success! Scene saved to {output_filepath}")

camera_obj = bpy.data.objects.get("Camera")
# --- Create and Configure the Constraint ---
# Make sure both the camera and target object exist
if camera_obj and obj:
    # Add a new 'Track To' constraint to the camera
    constraint = camera_obj.constraints.new(type='TRACK_TO')
    
    # Set the target of the constraint to our object
    constraint.target = obj
    
    # By default, cameras point down their -Z axis.
    # We tell the constraint to aim this axis at the target.
    constraint.track_axis = 'TRACK_NEGATIVE_Z'
    
    # We set the 'Up' axis to Y to keep the camera from rolling
    constraint.up_axis = 'UP_Y'
    
    print(f"Success! Camera is now tracking '{object_name}'.")

else:
    print(f"Error: Could not find camera Camera or target '{object_name}'.")


# Get a reference to the current scene
scene = bpy.context.scene

# --- Configure Render Settings ---

# Set the output path and file name.
# The .jpg extension is important here.
scene.render.filepath = os.path.join(WORKDIR, "output", "scene.jpg")


# Set the output file format to JPEG
scene.render.image_settings.file_format = 'JPEG'

# Set the quality for the JPEG (0-100)
scene.render.image_settings.quality = 90
scene.render.resolution_x = 640 # Default is 1920
scene.render.resolution_y = 640  # Default is 1080

# --- Render and Save the Image ---

# Trigger the render operation.
# 'write_still=True' tells Blender to save the image to the filepath.
bpy.context.scene.render.engine = 'BLENDER_EEVEE_NEXT'
scene.eevee.taa_render_samples = 16 # Default is 64
bpy.ops.render.render(write_still=True)

print(f"Success! Scene exported to {scene.render.filepath}")