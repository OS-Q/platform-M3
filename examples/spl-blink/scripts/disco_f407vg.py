Import("env")
import shutil
import os

def after_build(source, target, env):
	isExists=os.path.exists('build')
	if not isExists:
		os.mkdir('build')
	shutil.copy(firmware_source, 'build/spl_blink_f407vg.bin')

env.AddPostAction("buildprog", after_build)

firmware_source = os.path.join(env.subst("$BUILD_DIR"), "firmware.bin")
