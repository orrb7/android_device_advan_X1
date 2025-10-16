#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)

from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/advan/X1',
    'hardware/mediatek',
]

blob_fixups: blob_fixups_user_type = {
    'vendor/lib64/hw/audio.primary.mediatek.so': blob_fixup()
        .add_needed('libstagefright_foundation-v33.so'),
    'vendor/lib64/hw/mt6789/android.hardware.camera.provider@2.6-impl-mediatek.so': blob_fixup()
        .replace_needed('libutils.so', 'libutils-v32.so')
        .add_needed('libcamera_metadata_shim.so'),
    'vendor/lib64/mt6789/libmtkcam_stdutils.so': blob_fixup()
        .replace_needed('libutils.so', 'libutils-v32.so'),
    'vendor/etc/init/android.hardware.neuralnetworks-shim-service-mtk.rc': blob_fixup()
        .regex_replace('start', 'enable'),
    ('vendor/lib64/libwvhidl.so', 'vendor/lib64/mediadrm/libwvdrmengine.so'): blob_fixup()
        .replace_needed('libprotobuf-cpp-lite-3.9.1.so', 'libprotobuf-cpp-full-3.9.1.so'),
    'vendor/bin/hw/android.hardware.security.keymint-service.trustonic': blob_fixup()
        .add_needed('android.hardware.security.rkp-V3-ndk.so'),
    'vendor/lib64/hw/mt6789/vendor.mediatek.hardware.pq@2.15-impl.so': blob_fixup()
        .replace_needed('libutils.so', 'libutils-v32.so'),
}  # fmt: skip

module = ExtractUtilsModule(
    'X1',
    'advan',
    blob_fixups=blob_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
