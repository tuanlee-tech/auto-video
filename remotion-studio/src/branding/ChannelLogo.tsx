import React from 'react';
import { VectorStickman } from './DoodleIcons';

interface ChannelLogoProps {
  channelName?: string;
  badgeText?: string;
  showCircularGuide?: boolean;
}

export const ChannelLogo: React.FC<ChannelLogoProps> = ({
  channelName = 'Thói Quen Thịnh Vượng',
  badgeText = 'TQTV',
  showCircularGuide = false,
}) => {
  return (
    <div
      style={{
        width: 800,
        height: 800,
        background: '#FFFFFF',
        position: 'relative',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        overflow: 'hidden',
        boxSizing: 'border-box',
        fontFamily:
          "system-ui, -apple-system, BlinkMacSystemFont, 'Montserrat', sans-serif",
      }}
    >
      {/* Soft circular background accent */}
      <div
        style={{
          position: 'absolute',
          width: 680,
          height: 680,
          borderRadius: '50%',
          background: 'radial-gradient(circle, #F1F5F9 0%, #FFFFFF 75%)',
          zIndex: 1,
        }}
      />

      {/* Decorative floating doodles: Lightbulb, Sparkles, Dollar */}
      <div
        style={{
          position: 'absolute',
          top: 130,
          left: 140,
          fontSize: 42,
          zIndex: 5,
          transform: 'rotate(-12deg)',
        }}
      >
        💡
      </div>
      <div
        style={{
          position: 'absolute',
          top: 150,
          right: 150,
          fontSize: 38,
          zIndex: 5,
          color: '#F59E0B',
          fontWeight: 900,
        }}
      >
        ✦
      </div>
      <div
        style={{
          position: 'absolute',
          bottom: 140,
          left: 150,
          fontSize: 36,
          zIndex: 5,
          color: '#059669',
          fontWeight: 900,
        }}
      >
        $
      </div>
      <div
        style={{
          position: 'absolute',
          bottom: 150,
          right: 150,
          fontSize: 32,
          zIndex: 5,
        }}
      >
        📈
      </div>

      {/* Central Stickman Character: Waving cheerfully */}
      <div
        style={{
          position: 'relative',
          zIndex: 10,
          marginTop: -20,
          filter: 'drop-shadow(0 12px 24px rgba(0, 0, 0, 0.08))',
        }}
      >
        <VectorStickman pose="waving" size={440} />
      </div>

      {/* Optional YouTube 1:1 Circular Safe Area Overlay Guide */}
      {showCircularGuide && (
        <div
          style={{
            position: 'absolute',
            top: 20,
            left: 20,
            width: 760,
            height: 760,
            borderRadius: '50%',
            border: '3px dashed #CBD5E1',
            pointerEvents: 'none',
            zIndex: 30,
          }}
        />
      )}
    </div>
  );
};
