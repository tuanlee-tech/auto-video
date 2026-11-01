export interface WordTiming {
  word: string;
  start_ms: number;
  end_ms: number;
}

export interface SceneData {
  scene_id: number;
  spoken_text: string;
  audio_file: string;
  duration_sec: number;
  duration_frames: number;
  is_video_slot?: boolean;
  fixed_duration?: number;
  outfit_id?: number;
  outfit_name?: string;
  asset_file?: string;
  asset_type?: 'image' | 'video';
  video_start_offset_sec?: number;
  camera_motion?: 'zoom_in' | 'zoom_out' | 'pan_left' | 'pan_right';
  timing_file?: string;
  words?: WordTiming[];
}

export interface BgmConfig {
  mode?: 'single' | 'dual';
  track_1?: string;
  track_2?: string;
  transition_scene_id?: number;
  volume_ducked?: number;
  volume_normal?: number;
  fade_in_frames?: number;
  fade_out_frames?: number;
  primary_mood?: string;
  secondary_mood?: string;
}

export interface ManifestData {
  project_name: string;
  fps: number;
  width: number;
  height: number;
  aspect_ratio: string;
  audio_file?: string;
  bgm_file?: string;
  bgm_volume_ducked?: number;
  bgm_volume_normal?: number;
  bgm?: BgmConfig;
  scenes: SceneData[];
}

export interface CompositionProps {
  manifest?: ManifestData;
}
