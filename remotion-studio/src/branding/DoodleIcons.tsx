import React from 'react';

/**
 * High-precision hand-drawn vector doodle components inspired by "Simple Ways of Life".
 * Bold black ink outlines, clean cel-shaded colors, high contrast against white paper backgrounds.
 */

export const BrandBadge: React.FC<{ size?: number; label?: string }> = ({
  size = 54,
  label = 'TLTC',
}) => (
  <div
    style={{
      width: size,
      height: size,
      borderRadius: '50%',
      background: 'linear-gradient(135deg, #4F46E5 0%, #3730A3 100%)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      color: '#FFFFFF',
      fontWeight: 900,
      fontSize: size * 0.34,
      fontFamily: "'Montserrat', sans-serif",
      boxShadow: '0 4px 12px rgba(79, 70, 229, 0.35)',
      border: '3px solid #FFFFFF',
      letterSpacing: '0.05em',
    }}
  >
    {label}
  </div>
);

export const YellowHighlightBox: React.FC<{
  children: React.ReactNode;
  rotateDeg?: number;
  color?: string;
}> = ({ children, rotateDeg = -1.2, color = '#FFE600' }) => (
  <span
    style={{
      display: 'inline-block',
      position: 'relative',
      margin: '0 8px',
      transform: `rotate(${rotateDeg}deg)`,
      zIndex: 1,
    }}
  >
    <span
      style={{
        position: 'absolute',
        top: '-4px',
        left: '-16px',
        right: '-16px',
        bottom: '-4px',
        background: color,
        borderRadius: '8px',
        boxShadow: '0 6px 0px rgba(0, 0, 0, 0.12)',
        zIndex: -1,
      }}
    />
    <span
      style={{
        color: '#111827',
        fontWeight: 900,
        textTransform: 'uppercase',
        letterSpacing: '-0.02em',
      }}
    >
      {children}
    </span>
  </span>
);

export const DoodleArrow: React.FC<{
  width?: number;
  height?: number;
  color?: string;
  curved?: boolean;
}> = ({ width = 120, height = 50, color = '#111827', curved = true }) => (
  <svg
    width={width}
    height={height}
    viewBox="0 0 120 50"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
    style={{ overflow: 'visible' }}
  >
    {curved ? (
      <>
        <path
          d="M10 38C40 10 80 12 105 24"
          stroke={color}
          strokeWidth="6"
          strokeLinecap="round"
          strokeDasharray="1 1"
          style={{ strokeDasharray: 'none' }}
        />
        <path
          d="M92 14L108 26L92 36"
          stroke={color}
          strokeWidth="6"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </>
    ) : (
      <>
        <line
          x1="10"
          y1="25"
          x2="100"
          y2="25"
          stroke={color}
          strokeWidth="6"
          strokeLinecap="round"
        />
        <path
          d="M85 12L105 25L85 38"
          stroke={color}
          strokeWidth="6"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </>
    )}
  </svg>
);

export const DoodleMoneyBag: React.FC<{ size?: number }> = ({ size = 100 }) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 100 100"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
  >
    {/* Tied ribbon top */}
    <path
      d="M42 22C42 16 38 12 34 12C30 12 30 18 36 22H64C70 18 70 12 66 12C62 12 58 16 58 22"
      fill="#10B981"
      stroke="#111827"
      strokeWidth="4"
    />
    <rect
      x="38"
      y="22"
      width="24"
      height="8"
      rx="4"
      fill="#F59E0B"
      stroke="#111827"
      strokeWidth="4"
    />
    {/* Bag body */}
    <path
      d="M40 30C22 35 14 55 16 75C18 90 32 94 50 94C68 94 82 90 84 75C86 55 78 35 60 30H40Z"
      fill="#34D399"
      stroke="#111827"
      strokeWidth="5"
      strokeLinejoin="round"
    />
    {/* Dollar symbol */}
    <text
      x="50"
      y="70"
      fill="#065F46"
      fontSize="36"
      fontWeight="900"
      fontFamily="'Montserrat', sans-serif"
      textAnchor="middle"
    >
      $
    </text>
  </svg>
);

export const TwoBoxesDiagram: React.FC = () => (
  <div
    style={{
      display: 'flex',
      alignItems: 'center',
      gap: 32,
      background: 'rgba(248, 250, 252, 0.95)',
      padding: '28px 36px',
      borderRadius: '24px',
      border: '4px solid #111827',
      boxShadow: '8px 8px 0px #111827',
    }}
  >
    {/* Box 1: Spending */}
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        width: 220,
      }}
    >
      <div
        style={{
          width: 130,
          height: 110,
          background: '#FEF3C7',
          border: '4px solid #111827',
          borderRadius: '16px',
          boxShadow: '4px 4px 0px #111827',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          position: 'relative',
        }}
      >
        <span style={{ fontSize: 44 }}>☕</span>
        <div
          style={{
            position: 'absolute',
            top: -14,
            background: '#F59E0B',
            color: '#FFFFFF',
            fontSize: 13,
            fontWeight: 900,
            padding: '2px 10px',
            borderRadius: 8,
            border: '2px solid #111827',
          }}
        >
          HỘP 1
        </div>
      </div>
      <span
        style={{
          marginTop: 12,
          fontWeight: 900,
          fontSize: 18,
          color: '#111827',
          textAlign: 'center',
        }}
      >
        CHI TIÊU TỰ DO
      </span>
      <span style={{ fontSize: 13, color: '#64748B', fontWeight: 700 }}>
        Không cảm giác tội lỗi
      </span>
    </div>

    {/* Arrow Flow */}
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
      }}
    >
      <span
        style={{
          fontSize: 14,
          fontWeight: 900,
          color: '#2563EB',
          marginBottom: 4,
          letterSpacing: '0.04em',
        }}
      >
        TỰ ĐỘNG HÓA
      </span>
      <DoodleArrow width={100} height={40} color="#2563EB" />
    </div>

    {/* Box 2: Vault */}
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        width: 220,
      }}
    >
      <div
        style={{
          width: 130,
          height: 110,
          background: '#DBEAFE',
          border: '4px solid #111827',
          borderRadius: '16px',
          boxShadow: '4px 4px 0px #111827',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          position: 'relative',
        }}
      >
        <span style={{ fontSize: 44 }}>🔒</span>
        <div
          style={{
            position: 'absolute',
            top: -14,
            background: '#2563EB',
            color: '#FFFFFF',
            fontSize: 13,
            fontWeight: 900,
            padding: '2px 10px',
            borderRadius: 8,
            border: '2px solid #111827',
          }}
        >
          HỘP 2
        </div>
      </div>
      <span
        style={{
          marginTop: 12,
          fontWeight: 900,
          fontSize: 18,
          color: '#111827',
          textAlign: 'center',
        }}
      >
        TÍCH LŨY VÔ HÌNH
      </span>
      <span style={{ fontSize: 13, color: '#059669', fontWeight: 800 }}>
        Trích ngay khi lương về
      </span>
    </div>
  </div>
);

/**
 * Stylized Simple Ways of Life Vector Stickman Character.
 * Perfectly rendered with SVG vectors: thick black outlines, cel-shaded blue t-shirt, cheerful smile.
 */
export const VectorStickman: React.FC<{
  pose?: 'presenting' | 'waving' | 'running' | 'celebrating' | 'thinking';
  size?: number;
}> = ({ pose = 'presenting', size = 360 }) => {
  return (
    <svg
      width={size}
      height={size * 1.25}
      viewBox="0 0 240 300"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      style={{ overflow: 'visible' }}
    >
      {/* Dynamic Poses */}
      {pose === 'waving' && (
        <g>
          {/* Left waving arm */}
          <path
            d="M85 105C60 90 40 60 45 40C48 30 60 30 62 42C65 55 75 80 90 98"
            stroke="#111827"
            strokeWidth="8"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
          {/* Motion lines for wave */}
          <path
            d="M30 45C32 35 40 30 42 22"
            stroke="#111827"
            strokeWidth="4"
            strokeLinecap="round"
          />
          <path
            d="M22 55C25 45 32 40 35 32"
            stroke="#111827"
            strokeWidth="4"
            strokeLinecap="round"
          />

          {/* Right hand on hip */}
          <path
            d="M155 105C175 125 185 140 170 160C160 170 148 162 142 145"
            stroke="#111827"
            strokeWidth="8"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </g>
      )}

      {pose === 'presenting' && (
        <g>
          {/* Left arm presenting towards center/diagram */}
          <path
            d="M85 110C60 115 30 110 5 100"
            stroke="#111827"
            strokeWidth="8"
            strokeLinecap="round"
          />
          <circle cx="5" cy="100" r="7" fill="#FFFFFF" stroke="#111827" strokeWidth="6" />

          {/* Right arm thumbs up */}
          <path
            d="M155 110C180 105 195 85 190 70"
            stroke="#111827"
            strokeWidth="8"
            strokeLinecap="round"
          />
          <path
            d="M190 70C190 60 200 60 202 70"
            stroke="#111827"
            strokeWidth="8"
            strokeLinecap="round"
          />
        </g>
      )}

      {/* Legs & Shoes */}
      <g>
        {/* Left Leg */}
        <line x1="102" y1="180" x2="95" y2="255" stroke="#111827" strokeWidth="8" strokeLinecap="round" />
        {/* Left Shoe */}
        <path
          d="M80 262H110C112 262 114 256 110 252C102 248 90 248 85 252C80 256 76 262 80 262Z"
          fill="#FFFFFF"
          stroke="#111827"
          strokeWidth="6"
          strokeLinejoin="round"
        />

        {/* Right Leg */}
        <line x1="138" y1="180" x2="148" y2="255" stroke="#111827" strokeWidth="8" strokeLinecap="round" />
        {/* Right Shoe */}
        <path
          d="M135 262H165C167 262 169 256 165 252C157 248 145 248 140 252C135 256 131 262 135 262Z"
          fill="#FFFFFF"
          stroke="#111827"
          strokeWidth="6"
          strokeLinejoin="round"
        />
      </g>

      {/* Blue Athletic T-shirt Torso */}
      <g>
        <path
          d="M88 95L70 120L84 135L92 122V178H148V122L156 135L170 120L152 95C140 102 100 102 88 95Z"
          fill="#2563EB"
          stroke="#111827"
          strokeWidth="7"
          strokeLinejoin="round"
        />
        {/* Brand Circular Badge on Chest */}
        <circle cx="120" cy="132" r="14" fill="#FFFFFF" stroke="#111827" strokeWidth="3" />
        <circle cx="120" cy="132" r="10" fill="#1D4ED8" />
        <text
          x="120"
          y="135"
          fill="#FFFFFF"
          fontSize="7"
          fontWeight="900"
          fontFamily="'Montserrat', sans-serif"
          textAnchor="middle"
        >
          $
        </text>

        {/* Navy shorts */}
        <path
          d="M92 176H148V195H124L120 188L116 195H92V176Z"
          fill="#1E293B"
          stroke="#111827"
          strokeWidth="6"
          strokeLinejoin="round"
        />
      </g>

      {/* Characteristic Round Egg-shaped Head */}
      <g>
        <ellipse
          cx="120"
          cy="50"
          rx="42"
          ry="45"
          fill="#FFFFFF"
          stroke="#111827"
          strokeWidth="8"
        />

        {/* Happy Expressive Eyes */}
        <ellipse cx="108" cy="46" rx="5" ry="7" fill="#111827" />
        <ellipse cx="132" cy="46" rx="5" ry="7" fill="#111827" />

        {/* Light shine in eyes */}
        <circle cx="106" cy="43" r="2" fill="#FFFFFF" />
        <circle cx="130" cy="43" r="2" fill="#FFFFFF" />

        {/* Cheerful Eyebrows */}
        <path
          d="M101 34C105 31 113 32 116 35"
          stroke="#111827"
          strokeWidth="4"
          strokeLinecap="round"
        />
        <path
          d="M124 35C127 32 135 31 139 34"
          stroke="#111827"
          strokeWidth="4"
          strokeLinecap="round"
        />

        {/* Broad Enthusiastic Smile with Tongue */}
        <path
          d="M102 58C108 76 132 76 138 58Z"
          fill="#111827"
          stroke="#111827"
          strokeWidth="3"
        />
        <path
          d="M110 68C115 64 125 64 130 68C126 73 114 73 110 68Z"
          fill="#EF4444"
        />

        {/* Rosy cheeks */}
        <ellipse cx="96" cy="56" rx="6" ry="4" fill="#FECDD3" opacity="0.8" />
        <ellipse cx="144" cy="56" rx="6" ry="4" fill="#FECDD3" opacity="0.8" />
      </g>
    </svg>
  );
};
