#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)

from extract_utils.fixups_lib import (
    lib_fixups,
    lib_fixups_user_type,
)

from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/advan/X1',
    'hardware/mediatek',
    'hardware/mediatek/libmtkperf_client',
]

def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'vendor' else None


lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    ('vendor.mediatek.hardware.videotelephony@1.0',): lib_fixup_vendor_suffix,
}

blob_fixups: blob_fixups_user_type = {
    'system_ext/priv-app/ImsService/ImsService.apk': blob_fixup()
        .apktool_patch('blob-patches/ImsService'),
    'system_ext/lib64/libimsma.so': blob_fixup()
        .replace_needed('libsink.so', 'libsink-mtk.so'),
    'system_ext/lib64/libsink-mtk.so': blob_fixup()
        .add_needed('libaudioclient_shim.so'),
    'system_ext/lib64/libsource.so': blob_fixup()
        .add_needed('libui_shim.so'),
    'vendor/lib64/hw/audio.primary.mediatek.so': blob_fixup()
        .add_needed('libstagefright_foundation-v33.so'),
    'vendor/lib64/hw/mt6789/android.hardware.camera.provider@2.6-impl-mediatek.so': blob_fixup()
        .replace_needed('libutils.so', 'libutils-v32.so')
        .add_needed('libcamera_metadata_shim.so'),
    'vendor/lib64/mt6789/libmtkcam_stdutils.so': blob_fixup()
        .replace_needed('libutils.so', 'libutils-v32.so'),
    'vendor/bin/hw/android.hardware.media.c2@1.2-mediatek-64b': blob_fixup()
        .add_needed('libstagefright_foundation-v33.so')
        .replace_needed('libavservices_minijail_vendor.so', 'libavservices_minijail.so'),
    'vendor/etc/init/android.hardware.neuralnetworks-shim-service-mtk.rc': blob_fixup()
        .regex_replace('start', 'enable'),
    ('vendor/lib64/libwvhidl.so', 'vendor/lib64/mediadrm/libwvdrmengine.so'): blob_fixup()
        .replace_needed('libprotobuf-cpp-lite-3.9.1.so', 'libprotobuf-cpp-full-3.9.1.so'),
    'vendor/bin/hw/android.hardware.security.keymint-service.trustonic': blob_fixup()
        .add_needed('android.hardware.security.rkp-V3-ndk.so'),
    'vendor/bin/hw/mtkfusionrild' : blob_fixup()
        .add_needed('libutils-v32.so'),
    'vendor/lib64/hw/mt6789/vendor.mediatek.hardware.pq@2.15-impl.so': blob_fixup()
        .replace_needed('libutils.so', 'libutils-v32.so'),
    'vendor/etc/init/init.thermal_core.rc': blob_fixup()
        .regex_replace('ro.vendor.mtk_thermal_2_0', 'vendor.thermal.link_ready'),
    'vendor/etc/init/android.hardware.media.c2@1.2-mediatek.rc': blob_fixup()
        .add_line_if_missing('    interface android.hardware.media.c2@1.0::IComponentStore default')
        .add_line_if_missing('    interface android.hardware.media.c2@1.1::IComponentStore default')
        .add_line_if_missing('    interface android.hardware.media.c2@1.2::IComponentStore default')
        .regex_replace('@1.2-mediatek', '@1.2-mediatek-64b'),
    'vendor/etc/libnfc-hal-st.conf': blob_fixup()
        .regex_replace('STNFC_FW_DEBUG_ENABLED=1', 'STNFC_FW_DEBUG_ENABLED=0'),
}  # fmt: skip

module = ExtractUtilsModule(
    'X1',
    'advan',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
