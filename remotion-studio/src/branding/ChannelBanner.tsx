import React from 'react';
import { VectorStickman } from './DoodleIcons';

interface ChannelBannerProps {
  channelName?: string;
  tagline?: string;
  website?: string;
  showSafeZoneGuide?: boolean;
}

export const ChannelBanner: React.FC<ChannelBannerProps> = ({
  channelName = 'Thói Quen Thịnh Vượng',
  tagline = 'Hành động nhỏ, Tự chủ lớn • Xây dựng hệ thống, Chinh phục tự do',
  website = 'youtube.com/@thoiquenthinhvuong',
  showSafeZoneGuide = false,
}) => {
  return (
    <div
      style={{
        width: 2560,
        height: 1440,
        background: '#FFFFFF',
        backgroundImage: 'radial-gradient(#E2E8F0 1.5px, transparent 1.5px)',
        backgroundSize: '28px 28px',
        position: 'relative',
        overflow: 'hidden',
        boxSizing: 'border-box',
        fontFamily:
          "system-ui, -apple-system, BlinkMacSystemFont, 'Montserrat', 'Segoe UI', Roboto, sans-serif",
      }}
    >
      {/* 1. Panoramic Landscape SVG Artwork (Mountains, Hills, Winding Trail) */}
      <svg
        width="2560"
        height="1440"
        viewBox="0 0 2560 1440"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        style={{ position: 'absolute', top: 0, left: 0, zIndex: 2 }}
      >
        {/* Soft Background Distant Mountains (Watercolor Blue Wash) */}
        <path
          d="M0 880L280 680L520 820L840 590L1220 840L1680 540L2080 780L2360 620L2560 740V1440H0V880Z"
          fill="#EFF6FF"
          stroke="#BFDBFE"
          strokeWidth="3"
        />

        {/* Midground Mountain Ridges */}
        <path
          d="M0 960L380 780L720 940L1140 760L1520 920L1940 720L2280 890L2560 810V1440H0V960Z"
          fill="#DBEAFE"
          stroke="#93C5FD"
          strokeWidth="4"
        />

        {/* Gentle Rolling Hills (Soft Sage Green) */}
        <path
          d="M0 1060C450 940 850 1020 1280 980C1700 940 2150 1040 2560 990V1440H0V1060Z"
          fill="#F0FDF4"
          stroke="#86EFAC"
          strokeWidth="4"
        />

        {/* The Iconic Winding Mountain Trail / Journey of Life */}
        <path
          d="M100 1200C380 1100 480 940 740 920C1020 900 1200 970 1480 940C1760 910 1980 820 2260 760C2400 730 2500 710 2560 700"
          stroke="#D97706"
          strokeWidth="18"
          strokeLinecap="round"
          strokeDasharray="24 16"
          fill="none"
          opacity="0.85"
        />

        {/* Trail Boundary Outline */}
        <path
          d="M90 1208C370 1108 470 948 730 928C1010 908 1190 978 1470 948C1750 918 1970 828 2250 768C2390 738 2490 718 2560 708"
          stroke="#111827"
          strokeWidth="4"
          strokeLinecap="round"
          fill="none"
        />

        {/* Pine Trees along the Trail */}
        {/* Left trees */}
        <path d="M420 980L440 920L460 980H420Z" fill="#15803D" stroke="#111827" strokeWidth="3" />
        <path d="M480 990L500 935L520 990H480Z" fill="#16A34A" stroke="#111827" strokeWidth="3" />
        <path d="M780 950L800 890L820 950H780Z" fill="#15803D" stroke="#111827" strokeWidth="3" />
        {/* Right trees */}
        <path d="M1980 880L2000 810L2020 880H1980Z" fill="#15803D" stroke="#111827" strokeWidth="3" />
        <path d="M2140 840L2160 770L2180 840H2140Z" fill="#16A34A" stroke="#111827" strokeWidth="3" />

        {/* Hand-Drawn Sun in the Sky */}
        <circle cx="2160" cy="460" r="64" fill="#FEF08A" stroke="#111827" strokeWidth="5" />
        {/* Sun rays */}
        <line x1="2160" y1="360" x2="2160" y2="380" stroke="#111827" strokeWidth="5" strokeLinecap="round" />
        <line x1="2160" y1="540" x2="2160" y2="560" stroke="#111827" strokeWidth="5" strokeLinecap="round" />
        <line x1="2060" y1="460" x2="2080" y2="460" stroke="#111827" strokeWidth="5" strokeLinecap="round" />
        <line x1="2240" y1="460" x2="2260" y2="460" stroke="#111827" strokeWidth="5" strokeLinecap="round" />

        {/* Hand-Drawn Drifting Clouds */}
        <g stroke="#111827" strokeWidth="4" fill="#FFFFFF">
          <path d="M520 480C520 450 545 430 575 430C590 410 625 410 645 425C665 415 695 425 700 450C725 450 740 470 735 490C735 510 710 520 680 520H545C525 520 520 500 520 480Z" />
          <path d="M1580 440C1580 415 1600 395 1625 395C1640 380 1670 380 1685 395C1705 385 1730 395 1735 415C1755 415 1770 435 1765 450C1765 465 1745 475 1720 475H1600C1580 475 1580 460 1580 440Z" />
        </g>

        {/* Flying Birds */}
        <path d="M960 440C975 430 990 440 990 440C1005 430 1020 440 1020 440" stroke="#111827" strokeWidth="3" strokeLinecap="round" />
        <path d="M1040 420C1052 412 1064 420 1064 420C1076 412 1088 420 1088 420" stroke="#111827" strokeWidth="3" strokeLinecap="round" />
      </svg>

      {/* 2. YouTube Universal Safe Area Center Container (1546 x 423 px) */}
      <div
        style={{
          position: 'absolute',
          top: 508,
          left: 507,
          width: 1546,
          height: 423,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          padding: '0 50px',
          boxSizing: 'border-box',
          zIndex: 10,
        }}
      >
        {/* Left Stickman: Hiking the Trail */}
        <div
          style={{
            transform: 'scale(0.88)',
            filter: 'drop-shadow(6px 8px 0px rgba(0, 0, 0, 0.12))',
            marginTop: 20,
          }}
        >
          <VectorStickman pose="waving" size={310} />
        </div>

        {/* Center Title & Slogan Block */}
        <div
          style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            textAlign: 'center',
            maxWidth: 820,
          }}
        >
          {/* Main Channel Title in Hand-Lettered Display Style */}
          <div
            style={{
              fontSize: 68,
              fontWeight: 950,
              color: '#111827',
              letterSpacing: '-0.03em',
              textTransform: 'uppercase',
              textShadow: '0 3px 0px #FFE600, 0 6px 16px rgba(0,0,0,0.06)',
              marginBottom: 6,
            }}
          >
            {channelName}
          </div>

          {/* Yellow Highlighter Bar under title */}
          <div
            style={{
              width: 320,
              height: 8,
              background: '#FFE600',
              borderRadius: 4,
              marginBottom: 16,
              boxShadow: '0 2px 0px #111827',
            }}
          />

          {/* Tagline */}
          <div
            style={{
              fontSize: 22,
              fontWeight: 800,
              color: '#334155',
              letterSpacing: '0.01em',
              lineHeight: 1.4,
              marginBottom: 14,
            }}
          >
            {tagline}
          </div>

          {/* Brand Badge & Website Pill */}
          <div
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: 12,
              background: '#111827',
              color: '#FFFFFF',
              padding: '8px 24px',
              borderRadius: 50,
              fontSize: 16,
              fontWeight: 800,
              letterSpacing: '0.04em',
              boxShadow: '0 4px 10px rgba(0,0,0,0.18)',
            }}
          >
            <span style={{ color: '#FBBF24' }}>★</span>
            <span>{website}</span>
          </div>
        </div>

        {/* Right Stickman: Celebrating at Summit */}
        <div
          style={{
            transform: 'scale(0.88) scaleX(-1)', // Mirrored facing inward
            filter: 'drop-shadow(-6px 8px 0px rgba(0, 0, 0, 0.12))',
            marginTop: 20,
          }}
        >
          <VectorStickman pose="presenting" size={310} />
        </div>
      </div>

      {/* Optional Safe Area Outline Guide */}
      {showSafeZoneGuide && (
        <div
          style={{
            position: 'absolute',
            top: 508,
            left: 507,
            width: 1546,
            height: 423,
            border: '3px dashed #DC2626',
            pointerEvents: 'none',
            zIndex: 40,
            display: 'flex',
            alignItems: 'flex-start',
            justifyContent: 'flex-start',
            padding: 10,
          }}
        >
          <span
            style={{
              background: '#DC2626',
              color: '#FFFFFF',
              fontSize: 14,
              fontWeight: 900,
              padding: '2px 8px',
              borderRadius: 4,
            }}
          >
            YOUTUBE SAFE AREA (1546 x 423)
          </span>
        </div>
      )}
    </div>
  );
};
