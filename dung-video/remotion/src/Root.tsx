import React from 'react';
import {
  AbsoluteFill, Composition, Img, interpolate, Easing, spring, staticFile,
  useCurrentFrame, useVideoConfig,
} from 'remotion';
import '@fontsource/fredoka/600.css';

type ChuyenDong = {kieu: 'kb' | 'dam' | 'truot'; goc?: string; x?: number; y?: number};
type Hinh = {id: string; anh: string; bat_dau: number; chuyen_dong: ChuyenDong};
type Chu = {h: string; kieu: 'chu' | 'so' | 'nhan'; text: string; sub?: string; t: number; x: number; y: number; nen?: 'anh' | 'trang'};
type Bang = {fps: number; ket_thuc: number; hinh: Hinh[]; chu: Chu[]};

const FADE = 0.3; // chuyển mờ giữa các hình (giây)
const FONT = 'Fredoka';

const Lop: React.FC<{h: Hinh; ketThuc: number; dau: boolean}> = ({h, ketThuc, dau}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = f / fps - h.bat_dau;
  const dai = ketThuc - h.bat_dau;
  if (t < 0 || t > dai + FADE) return null;
  const cd = h.chuyen_dong;
  let opacity = dau ? 1 : interpolate(t, [0, FADE], [0, 1], {extrapolateRight: 'clamp'});
  let transform = '';
  let origin = 'center center';
  if (cd.kieu === 'kb') {
    const s = interpolate(t, [0, dai + FADE], [1.04, 1.1]);
    origin = {center: 'center center', left: '20% 50%', right: '80% 50%', top: '50% 20%'}[cd.goc ?? 'center'] ?? 'center center';
    transform = `scale(${s})`;
  } else if (cd.kieu === 'dam') {
    const nhanh = interpolate(t, [0, 0.35], [1.02, 1.16], {extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic)});
    const troi = interpolate(t, [0.35, dai + FADE], [0, 0.04], {extrapolateLeft: 'clamp'});
    origin = `${cd.x}% ${cd.y}%`;
    transform = `scale(${nhanh + troi})`;
  } else if (cd.kieu === 'truot') {
    opacity = 1;
    const x = interpolate(t, [0, 0.4], [100, 0], {extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic)});
    const s = interpolate(t, [0, dai + FADE], [1.04, 1.08]);
    transform = `translateX(${x}%) scale(${s})`;
  }
  return (
    <AbsoluteFill style={{opacity, overflow: 'hidden'}}>
      <Img src={staticFile(h.anh)} style={{width: '100%', height: '100%', objectFit: 'cover', transform, transformOrigin: origin}} />
    </AbsoluteFill>
  );
};

const LopChu: React.FC<{c: Chu; het: number}> = ({c, het}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = f / fps - c.t;
  if (t < 0 || f / fps > het) return null;
  const tat = interpolate(f / fps, [het - 0.15, het], [1, 0], {extrapolateLeft: 'clamp'});
  const nay = spring({frame: Math.round(t * fps), fps, config: {damping: 11, stiffness: 180}});
  const base: React.CSSProperties = {position: 'absolute', left: c.x, top: c.y, transform: 'translate(-50%,-50%)', fontFamily: FONT, fontWeight: 600, whiteSpace: 'nowrap', opacity: tat};
  if (c.kieu === 'chu') {
    const toc = Math.min(Math.max(c.text.length * 0.035, 0.25), 0.6);
    const n = Math.ceil(interpolate(t, [0, toc], [0, c.text.length], {extrapolateRight: 'clamp'}));
    const trenAnh = c.nen === 'anh';
    return (
      <div style={{...base, fontSize: 112, color: trenAnh ? 'white' : '#111',
        WebkitTextStroke: trenAnh ? '14px #111' : '14px white', paintOrder: 'stroke fill',
        textShadow: trenAnh ? '0 6px 0 rgba(0,0,0,0.35)' : '3px 4px 0 rgba(0,0,0,0.12)'}}>
        {c.text.slice(0, n)}
      </div>
    );
  }
  if (c.kieu === 'so') {
    return (
      <div style={{...base, transform: `translate(-50%,-50%) scale(${nay})`, textAlign: 'center'}}>
        <div style={{fontSize: 150, color: 'white', WebkitTextStroke: '16px #111', paintOrder: 'stroke fill', lineHeight: 1}}>{c.text}</div>
        <div style={{fontSize: 44, color: 'white', WebkitTextStroke: '9px #111', paintOrder: 'stroke fill', letterSpacing: 4, marginTop: 6}}>{c.sub}</div>
      </div>
    );
  }
  // nhan: thẻ trắng viền đen, hơi nghiêng
  return (
    <div style={{...base, transform: `translate(-50%,-50%) scale(${nay}) rotate(-2deg)`, fontSize: 62, color: '#111',
      background: 'white', border: '6px solid #111', borderRadius: 18, padding: '6px 28px', boxShadow: '6px 8px 0 rgba(0,0,0,0.25)'}}>
      {c.text}
    </div>
  );
};

const Video: React.FC<{bang: Bang}> = ({bang}) => {
  const hinh = bang.hinh;
  const hetHinh = (id: string) => {
    const i = hinh.findIndex((h) => h.id === id);
    return i + 1 < hinh.length ? hinh[i + 1].bat_dau : bang.ket_thuc;
  };
  return (
    <AbsoluteFill style={{background: 'white'}}>
      {hinh.map((h, i) => (
        <Lop key={h.id} h={h} dau={i === 0} ketThuc={i + 1 < hinh.length ? hinh[i + 1].bat_dau : bang.ket_thuc} />
      ))}
      {bang.chu.map((c, i) => <LopChu key={i} c={c} het={hetHinh(c.h)} />)}
    </AbsoluteFill>
  );
};

export const Root: React.FC = () => (
  <Composition
    id="Video"
    component={Video as any}
    fps={30}
    width={1920}
    height={1080}
    durationInFrames={300}
    defaultProps={{bang: {fps: 30, ket_thuc: 10, hinh: [], chu: []}}}
    calculateMetadata={({props}: any) => ({durationInFrames: Math.ceil(props.bang.ket_thuc * 30)})}
  />
);
