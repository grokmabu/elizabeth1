import React from 'react';
import {
  AbsoluteFill, Composition, Img, interpolate, Easing, spring, staticFile,
  useCurrentFrame, useVideoConfig,
} from 'remotion';
import '@fontsource/fredoka/600.css';

// ---------- Kiểu dữ liệu bảng dựng ----------
type ChuyenDong = {kieu: 'kb' | 'dam' | 'truot'; goc?: string; x?: number; y?: number};
// vao = kiểu chuyển cảnh ĐI VÀO hình này (hình trước tự đi ra cho khớp)
type Vao = 'mo' | 'trai' | 'phai' | 'len' | 'quet' | 'quet_trai' | 'lat' | 'zoom' | 'cat';
type Hinh = {id: string; anh: string; bat_dau: number; chuyen_dong: ChuyenDong; vao?: Vao};
type HieuChu = 'pop' | 'mo' | 'truot' | 'lo' | 'go' | 'dap';
type Chu = {h: string; kieu: 'chu' | 'so' | 'nhan'; text: string; sub?: string; t: number; x: number; y: number;
  nen?: 'anh' | 'trang'; hieu?: HieuChu; tu?: 'trai' | 'phai' | 'duoi'; mau?: 'vang' | 'do'; het?: number};
// nhan = điểm nhấn giọng: dap (phóng giật + rung), rung, flash, bat (chủ thể bật ra khỏi khung)
type Nhan = {t: number; kieu: 'dap' | 'rung' | 'flash' | 'bat'; manh?: number; x?: number; y?: number; w?: number; h?: number; anh?: string; dai?: number};
type Bang = {fps: number; ket_thuc: number; hinh: Hinh[]; chu: Chu[]; nhan?: Nhan[]};

const FONT = 'Fredoka';
const DUR: Record<Vao, number> = {mo: 0.3, trai: 0.42, phai: 0.42, len: 0.42, quet: 0.38, quet_trai: 0.38, lat: 0.5, zoom: 0.4, cat: 0.001};
const vaoCua = (h: Hinh): Vao => h.vao ?? (h.chuyen_dong.kieu === 'truot' ? 'trai' : 'mo');
const MAU = {vang: '#FFD21F', do: '#FF4B3E'};
const ease = Easing.inOut(Easing.cubic);
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;

// ---------- Một hình: chuyển động bên trong + chuyển cảnh vào/ra ----------
const Lop: React.FC<{h: Hinh; ketThuc: number; dau: boolean; ra?: Vao}> = ({h, ketThuc, dau, ra}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const now = f / fps;
  const t = now - h.bat_dau;
  const vao = dau ? 'cat' : vaoCua(h);
  const dRa = ra ? DUR[ra] : 0;
  if (t < 0 || now > ketThuc + dRa) return null;
  const dai = ketThuc - h.bat_dau + dRa;

  // chuyển động bên trong ảnh
  const cd = h.chuyen_dong;
  let inner = '';
  let origin = 'center center';
  if (cd.kieu === 'dam') {
    const nhanh = interpolate(t, [0, 0.35], [1.02, 1.16], {...clamp, easing: Easing.out(Easing.cubic)});
    const troi = interpolate(t, [0.35, dai], [0, 0.04], clamp);
    origin = `${cd.x}% ${cd.y}%`;
    inner = `scale(${nhanh + troi})`;
  } else {
    const s = interpolate(t, [0, dai], [1.04, 1.1]);
    origin = {center: 'center center', left: '20% 50%', right: '80% 50%', top: '50% 20%'}[cd.goc ?? 'center'] ?? 'center center';
    inner = `scale(${s})`;
  }

  // chuyển cảnh vào
  const pv = interpolate(t, [0, DUR[vao]], [0, 1], {...clamp, easing: ease});
  let opacity = 1, outer = '', clip = 'none';
  switch (vao) {
    case 'mo': opacity = pv; break;
    case 'trai': outer = `translateX(${(1 - pv) * 100}%)`; break;
    case 'phai': outer = `translateX(${-(1 - pv) * 100}%)`; break;
    case 'len': outer = `translateY(${(1 - pv) * 100}%)`; break;
    case 'quet': clip = `inset(0 0 0 ${(1 - pv) * 100}%)`; break;
    case 'quet_trai': clip = `inset(0 ${(1 - pv) * 100}% 0 0)`; break;
    case 'lat': {
      const nua = interpolate(t, [DUR.lat / 2, DUR.lat], [-90, 0], {...clamp, easing: Easing.out(Easing.cubic)});
      opacity = t < DUR.lat / 2 ? 0 : 1;
      outer = `perspective(2200px) rotateY(${nua}deg)`; break;
    }
    case 'zoom': opacity = pv; outer = `scale(${1.35 - 0.35 * pv})`; break;
  }

  // chuyển cảnh ra (khớp với kiểu vào của hình sau)
  if (ra) {
    const tr = now - ketThuc;
    const pr = interpolate(tr, [0, dRa], [0, 1], {...clamp, easing: ease});
    if (tr >= 0) {
      if (ra === 'trai') outer = `translateX(${-pr * 100}%)`;
      else if (ra === 'phai') outer = `translateX(${pr * 100}%)`;
      else if (ra === 'len') outer = `translateY(${-pr * 100}%)`;
      else if (ra === 'lat') {
        const nua = interpolate(tr, [0, DUR.lat / 2], [0, 90], {...clamp, easing: Easing.in(Easing.cubic)});
        outer = `perspective(2200px) rotateY(${nua}deg)`; opacity = tr < DUR.lat / 2 ? 1 : 0;
      } else if (ra === 'zoom') { outer = `scale(${1 + pr * 0.9})`; opacity = 1 - pr; }
    }
  }
  return (
    <AbsoluteFill style={{opacity, overflow: 'hidden', transform: outer, clipPath: clip, background: 'white'}}>
      <Img src={staticFile(h.anh)} style={{width: '100%', height: '100%', objectFit: 'cover', transform: inner, transformOrigin: origin}} />
    </AbsoluteFill>
  );
};

// ---------- Chữ ----------
const LopChu: React.FC<{c: Chu; het: number}> = ({c, het}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const now = f / fps;
  const t = now - c.t;
  const ketThuc = c.het ?? het;
  if (t < 0 || now > ketThuc) return null;
  const hieu: HieuChu = c.hieu ?? (c.kieu === 'chu' ? 'go' : 'pop');
  const tat = interpolate(now, [ketThuc - 0.18, ketThuc], [1, 0], clamp);
  const nay = spring({frame: Math.round(t * fps), fps, config: {damping: 11, stiffness: 180}});
  let tf = 'translate(-50%,-50%)';
  let op = tat;
  let clip = 'none';
  let text = c.text;
  if (hieu === 'pop') tf += ` scale(${nay})`;
  else if (hieu === 'mo') {
    op *= interpolate(t, [0, 0.3], [0, 1], clamp);
    tf += ` translateY(${interpolate(t, [0, 0.35], [24, 0], {...clamp, easing: Easing.out(Easing.cubic)})}px)`;
  } else if (hieu === 'truot') {
    const d = spring({frame: Math.round(t * fps), fps, config: {damping: 14, stiffness: 160}});
    const tu = c.tu ?? 'trai';
    const kc = (1 - d) * (tu === 'duoi' ? 260 : 700);
    tf += tu === 'trai' ? ` translateX(${-kc}px)` : tu === 'phai' ? ` translateX(${kc}px)` : ` translateY(${kc}px)`;
    op *= interpolate(t, [0, 0.12], [0, 1], clamp);
  } else if (hieu === 'lo') {
    const p = interpolate(t, [0, 0.4], [0, 100], {...clamp, easing: Easing.out(Easing.cubic)});
    clip = `inset(-30% ${100 - p}% -30% -10%)`;
  } else if (hieu === 'dap') {
    const s = interpolate(t, [0, 0.12], [2.6, 1], {...clamp, easing: Easing.in(Easing.quad)});
    const nay2 = t > 0.12 ? 1 + 0.08 * Math.exp(-(t - 0.12) * 12) * Math.cos((t - 0.12) * 40) : s;
    tf += ` scale(${nay2}) rotate(-3deg)`;
    op *= interpolate(t, [0, 0.06], [0, 1], clamp);
  } else if (hieu === 'go') {
    const toc = Math.min(Math.max(c.text.length * 0.025, 0.2), 0.4);
    text = c.text.slice(0, Math.ceil(interpolate(t, [0, toc], [0, c.text.length], clamp)));
  }
  const base: React.CSSProperties = {position: 'absolute', left: c.x, top: c.y, transform: tf, opacity: op, clipPath: clip,
    fontFamily: FONT, fontWeight: 600, whiteSpace: 'nowrap'};
  const mau = c.mau ? MAU[c.mau] : null;
  if (c.kieu === 'chu') {
    const trenAnh = c.nen === 'anh' || !!mau;
    return (
      <div style={{...base, fontSize: 112, color: mau ?? (trenAnh ? 'white' : '#111'),
        WebkitTextStroke: trenAnh ? '14px #111' : '14px white', paintOrder: 'stroke fill',
        textShadow: trenAnh ? '0 6px 0 rgba(0,0,0,0.35)' : '3px 4px 0 rgba(0,0,0,0.12)'}}>
        {text}
      </div>
    );
  }
  if (c.kieu === 'so') {
    return (
      <div style={{...base, textAlign: 'center'}}>
        <div style={{fontSize: 150, color: mau ?? 'white', WebkitTextStroke: '16px #111', paintOrder: 'stroke fill', lineHeight: 1}}>{text}</div>
        {c.sub ? <div style={{fontSize: 44, color: 'white', WebkitTextStroke: '9px #111', paintOrder: 'stroke fill', letterSpacing: 4, marginTop: 6}}>{c.sub}</div> : null}
      </div>
    );
  }
  return (
    <div style={{...base, transform: `${tf} rotate(-2deg)`, fontSize: 62, color: '#111',
      background: mau ?? 'white', border: '6px solid #111', borderRadius: 18, padding: '6px 28px', boxShadow: '6px 8px 0 rgba(0,0,0,0.25)'}}>
      {text}
    </div>
  );
};

// ---------- Điểm nhấn giọng ----------
const giat = (t: number, dai: number) => (t < 0 || t > dai ? 0 : t < 0.07 ? t / 0.07 : Math.exp(-(t - 0.07) * 7));

const khungNhan = (nhan: Nhan[], now: number) => {
  let s = 1, x = 0, y = 0, ox = 50, oy = 50;
  for (const n of nhan) {
    const t = now - n.t; const m = n.manh ?? 1;
    if (t < 0 || t > 0.9) continue;
    if (n.kieu === 'dap') {
      s += 0.14 * m * giat(t, 0.9); ox = n.x ?? 50; oy = n.y ?? 50;
    }
    if (n.kieu === 'dap' || n.kieu === 'rung') {
      const a = 22 * m * Math.exp(-t * 7);
      x += a * Math.sin(t * 95); y += a * 0.7 * Math.cos(t * 71);
    }
  }
  return {transform: `translate(${x}px,${y}px) scale(${s})`, transformOrigin: `${ox}% ${oy}%`};
};

const LopNhan: React.FC<{n: Nhan}> = ({n}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = f / fps - n.t;
  if (n.kieu === 'flash') {
    if (t < 0 || t > 0.3) return null;
    return <AbsoluteFill style={{background: 'white', opacity: interpolate(t, [0, 0.03, 0.3], [0, 0.75 * (n.manh ?? 1), 0], clamp)}} />;
  }
  if (n.kieu === 'bat' && n.anh) {
    const dai = n.dai ?? 1.3;
    if (t < 0 || t > dai) return null;
    const w = n.w ?? 40, h = n.h ?? 50, cx = n.x ?? 50, cy = n.y ?? 50;
    const vao = spring({frame: Math.round(t * fps), fps, config: {damping: 9, stiffness: 170}});
    const ra = interpolate(t, [dai - 0.2, dai], [1, 0], clamp);
    const s = 1 + 0.32 * vao * ra;
    const left = (cx - w / 2) * 19.2, top = (cy - h / 2) * 10.8, W = w * 19.2, H = h * 10.8;
    return (
      <AbsoluteFill>
        <AbsoluteFill style={{background: 'rgba(0,0,0,0.28)', opacity: vao * ra}} />
        <div style={{position: 'absolute', left, top, width: W, height: H, overflow: 'hidden', borderRadius: 26,
          border: '10px solid white', outline: '6px solid #111', boxShadow: '14px 18px 0 rgba(0,0,0,0.3)',
          transform: `scale(${s}) rotate(${-2 * vao * ra}deg)`, transformOrigin: 'center center', opacity: ra}}>
          <Img src={staticFile(n.anh)} style={{position: 'absolute', width: 1920, height: 1080,
            left: -left - 10, top: -top - 10, objectFit: 'cover', maxWidth: 'none'}} />
        </div>
      </AbsoluteFill>
    );
  }
  return null;
};

const Video: React.FC<{bang: Bang}> = ({bang}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const now = f / fps;
  const hinh = bang.hinh;
  const nhan = bang.nhan ?? [];
  const hetHinh = (id: string) => {
    const i = hinh.findIndex((h) => h.id === id);
    return i + 1 < hinh.length ? hinh[i + 1].bat_dau : bang.ket_thuc;
  };
  // chỉ dựng các hình đang có mặt quanh thời điểm hiện tại cho nhẹ
  const lop = hinh.map((h, i) => ({h, i})).filter(({h, i}) => {
    const kt = i + 1 < hinh.length ? hinh[i + 1].bat_dau + 0.6 : bang.ket_thuc;
    return now >= h.bat_dau - 0.05 && now <= kt;
  });
  return (
    <AbsoluteFill style={{background: 'white', overflow: 'hidden'}}>
      <AbsoluteFill style={khungNhan(nhan, now)}>
        {lop.map(({h, i}) => (
          <Lop key={h.id} h={h} dau={i === 0}
            ketThuc={i + 1 < hinh.length ? hinh[i + 1].bat_dau : bang.ket_thuc}
            ra={i + 1 < hinh.length ? vaoCua(hinh[i + 1]) : undefined} />
        ))}
        {bang.chu.filter((c) => now >= c.t - 0.05 && now <= (c.het ?? hetHinh(c.h)) + 0.05)
          .map((c, i) => <LopChu key={c.h + c.t + i} c={c} het={hetHinh(c.h)} />)}
      </AbsoluteFill>
      {nhan.filter((n) => n.kieu === 'flash' || n.kieu === 'bat').map((n, i) => <LopNhan key={i} n={n} />)}
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
    defaultProps={{bang: {fps: 30, ket_thuc: 10, hinh: [], chu: [], nhan: []}}}
    calculateMetadata={({props}: any) => ({durationInFrames: Math.ceil(props.bang.ket_thuc * 30)})}
  />
);
