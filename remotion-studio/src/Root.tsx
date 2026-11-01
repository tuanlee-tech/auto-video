import React from 'react';
import { Composition, Still, getInputProps } from 'remotion';
import { MainComposition } from './MainComposition';
import { defaultProjectData } from './defaultProps';
import { ManifestData } from './types';
import { Thumbnail } from './branding/Thumbnail';
import { ChannelLogo } from './branding/ChannelLogo';
import { ChannelBanner } from './branding/ChannelBanner';

export const Root: React.FC = () => {
  const inputProps = getInputProps() as { manifest?: ManifestData };
  const manifest = inputProps?.manifest || defaultProjectData;

  const fps = manifest.fps || 60;
  const width = manifest.width || 1920;
  const height = manifest.height || 1080;

  // Dynamically calculate total composition duration from scenes
  const totalFrames =
    manifest.scenes && manifest.scenes.length > 0
      ? manifest.scenes.reduce(
          (acc, s) =>
            acc + (s.duration_frames || Math.round((s.duration_sec || 3) * fps)),
          0
        )
      : 300;

  return (
    <>
      {/* 60FPS Main Video Engine */}
      <Composition
        id="MainComposition"
        component={MainComposition}
        durationInFrames={Math.max(totalFrames, 60)}
        fps={fps}
        width={width}
        height={height}
        defaultProps={{
          manifest,
        }}
      />

      {/* YouTube Thumbnail: 1920x1080 (16:9) Simple Ways of Life Style */}
      <Still
        id="Thumbnail"
        component={Thumbnail}
        width={1920}
        height={1080}
        defaultProps={{
          title: 'HỆ THỐNG TÀI CHÍNH',
          subtitle: 'QUY TẮC 2 CHIẾC HỘP',
          hook: 'DỪNG TIÊU HOANG • TỰ ĐỘNG LÀM GIÀU',
          badgeText: 'TQTV',
        }}
      />

      {/* YouTube Channel Avatar / Logo: 800x800 (1:1) */}
      <Still
        id="ChannelLogo"
        component={ChannelLogo}
        width={800}
        height={800}
        defaultProps={{
          channelName: 'Thói Quen Thịnh Vượng',
          badgeText: 'TQTV',
        }}
      />

      {/* YouTube Channel Banner: 2560x1440 with Universal Safe Zone */}
      <Still
        id="ChannelBanner"
        component={ChannelBanner}
        width={2560}
        height={1440}
        defaultProps={{
          channelName: 'Thói Quen Thịnh Vượng',
          tagline: 'Hành động nhỏ, Tự chủ lớn • Xây dựng hệ thống, Chinh phục tự do',
          website: 'youtube.com/@thoiquenthinhvuong',
        }}
      />
    </>
  );
};
