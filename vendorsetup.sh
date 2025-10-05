#!/bin/bash

echo "- Applying fenrir compatiblity patches"
cd system/core
curl https://github.com/Nothing-2A/android_system_core/commit/8ff6e7a68523c3b870d8dcd5713c71ea15b43dd2.patch | git am
curl https://github.com/Nothing-2A/android_system_core/commit/0d5990a96c5e6a404887f5575c5d00bcbbaaef74.patch | git am
cd ../../

echo "- Applying Aperture Mediatek HFPS Mode Patch"
cd packages/apps/Aperture
curl https://github.com/Nothing-2A/android_packages_apps_Aperture/commit/a4c34aa57ed56de60f29349a1e6d20cf8160ca15.patch | git am
cd ../../../
