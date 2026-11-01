import { ManifestData } from './types';
import syncedManifest from '../public/project_assets/manifest.json';

export const defaultProjectData: ManifestData = (syncedManifest as unknown as ManifestData) || {
  project_name: 'default_project',
  fps: 60,
  width: 1920,
  height: 1080,
  aspect_ratio: '16:9',
  scenes: [],
};
