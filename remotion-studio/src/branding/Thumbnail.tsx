import React from 'react';
import {
  BrandBadge,
  YellowHighlightBox,
  TwoBoxesDiagram,
  VectorStickman,
  DoodleArrow,
  DoodleMoneyBag,
} from './DoodleIcons';

interface ThumbnailProps {
  title?: string;
  subtitle?: string;
  hook?: string;
  badgeText?: string;
}

export const Thumbnail: React.FC<ThumbnailProps> = ({
  title = 'HỆ THỐNG TÀI CHÍNH',
  subtitle = 'QUY TẮC 2 CHIẾC HỘP',
  hook = 'DỪNG TIÊU HOANG • TỰ ĐỘNG LÀM GIÀU',
  badgeText = 'TLTC',
}) => {
  return (
    <div
      style={{
        width: 1920,
        height: 1080,
        background: '#FFFFFF',
        backgroundImage:
          'radial-gradient(#E2E8F0 2px, transparent 2px)',
        backgroundSize: '32px 32px',
        position: 'relative',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'space-between',
        padding: '70px 90px',
        fontFamily:
          "system-ui, -apple-system, BlinkMacSystemFont, 'Montserrat', 'Segoe UI', Roboto, sans-serif",
        overflow: 'hidden',
        boxSizing: 'border-box',
      }}
    >
      {/* Top Header Row */}
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'flex-start',
          zIndex: 10,
        }}
      >
        {/* Main Hook & Title Block */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 18 }}>
          {/* Small Top Tag */}
          <div
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: 10,
              background: '#111827',
              color: '#FFFFFF',
              padding: '8px 24px',
              borderRadius: 50,
              fontSize: 22,
              fontWeight: 900,
              letterSpacing: '0.06em',
              alignSelf: 'flex-start',
              boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
            }}
          >
            <span>🧠</span>
            <span>TÂM LÝ NÃO BỘ & TIỀN BẠC</span>
          </div>

          {/* Huge Main Headline with Signature Yellow Highlighter */}
          <div style={{ fontSize: 92, lineHeight: 1.1, marginTop: 4 }}>
            <YellowHighlightBox rotateDeg={-1.4} color="#FFE600">
              {title}
            </YellowHighlightBox>
          </div>

          {/* Crimson / Dark Subtitle */}
          <div
            style={{
              fontSize: 62,
              fontWeight: 950,
              color: '#E11D48',
              letterSpacing: '-0.02em',
              display: 'flex',
              alignItems: 'center',
              gap: 16,
            }}
          >
            <span>{subtitle}</span>
            <span style={{ fontSize: 44, color: '#F59E0B' }}>✦</span>
          </div>
        </div>

        {/* Top Right Brand Pill Badge */}
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end', gap: 12 }}>
          <BrandBadge size={68} label={badgeText} />
          <span
            style={{
              fontSize: 14,
              fontWeight: 900,
              color: '#64748B',
              letterSpacing: '0.08em',
              textTransform: 'uppercase',
            }}
          >
            Simple Ways of Life
          </span>
        </div>
      </div>

      {/* Center Main Stage: Two Boxes Diagram & Floating Doodles */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'flex-start',
          gap: 60,
          marginTop: -20,
          zIndex: 5,
        }}
      >
        {/* Interactive Two Boxes Diagram */}
        <div style={{ transform: 'scale(1.22)', transformOrigin: 'left center' }}>
          <TwoBoxesDiagram />
        </div>

        {/* Floating Money Bag & Callout Arrow */}
        <div
          style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            marginLeft: 50,
          }}
        >
          <div style={{ transform: 'rotate(12deg)' }}>
            <DoodleMoneyBag size={110} />
          </div>
          <span
            style={{
              fontSize: 20,
              fontWeight: 900,
              color: '#059669',
              background: '#D1FAE5',
              padding: '6px 16px',
              borderRadius: 12,
              border: '2px solid #059669',
              marginTop: 8,
              transform: 'rotate(-4deg)',
              boxShadow: '3px 3px 0px #059669',
            }}
          >
            +10x DÒNG TIỀN
          </span>
        </div>
      </div>

      {/* Bottom Bar: High-contrast callout & Stickman */}
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'flex-end',
          zIndex: 10,
        }}
      >
        {/* Bottom Punchy Banner */}
        <div
          style={{
            background: '#111827',
            color: '#FFFFFF',
            padding: '16px 36px',
            borderRadius: 18,
            border: '4px solid #111827',
            boxShadow: '6px 6px 0px #F59E0B',
            display: 'flex',
            alignItems: 'center',
            gap: 18,
            maxWidth: 1050,
          }}
        >
          <span style={{ fontSize: 32 }}>💡</span>
          <span
            style={{
              fontSize: 30,
              fontWeight: 900,
              letterSpacing: '-0.01em',
              textTransform: 'uppercase',
              color: '#FDE047',
            }}
          >
            {hook}
          </span>
        </div>

        {/* Little hand-drawn star decoration */}
        <div style={{ fontSize: 44, color: '#2563EB', marginBottom: 20, marginRight: 280 }}>
          ✦
        </div>
      </div>

      {/* Right Stickman Character: Energetic & Pointing */}
      <div
        style={{
          position: 'absolute',
          right: 50,
          bottom: 20,
          zIndex: 20,
          filter: 'drop-shadow(10px 14px 0px rgba(0, 0, 0, 0.14))',
        }}
      >
        <VectorStickman pose="presenting" size={480} />
      </div>

      {/* Subtle Hand-Drawn Arrow Pointing from Stickman to the Boxes */}
      <div
        style={{
          position: 'absolute',
          right: 480,
          bottom: 260,
          zIndex: 15,
          transform: 'rotate(-15deg)',
        }}
      >
        <DoodleArrow width={130} height={60} color="#2563EB" />
        <span
          style={{
            position: 'absolute',
            top: -26,
            left: 10,
            fontSize: 18,
            fontWeight: 900,
            color: '#2563EB',
            whiteSpace: 'nowrap',
          }}
        >
          CƠ CHẾ NÀY!
        </span>
      </div>
    </div>
  );
};
