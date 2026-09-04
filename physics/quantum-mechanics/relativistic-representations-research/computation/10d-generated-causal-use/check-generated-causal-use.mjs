import { pathToFileURL } from 'node:url';
import {
  constructBosonicFieldSystem,
  polynomialText,
} from '../10c-generative-residual-constructor/residual-constructor.mjs';

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function bump(value) {
  if (Math.abs(value) >= 1) return 0;
  return Math.exp(-1 / (1 - value * value));
}

function bumpDerivative(value) {
  if (Math.abs(value) >= 1) return 0;
  const denominator = 1 - value * value;
  return bump(value) * (-2 * value) / (denominator * denominator);
}

function simpson(f, left, right, intervals) {
  assert(intervals > 0 && intervals % 2 === 0, 'Simpson intervals must be positive and even');
  const step = (right - left) / intervals;
  let sum = f(left) + f(right);
  for (let index = 1; index < intervals; index += 1) {
    sum += (index % 2 === 0 ? 2 : 4) * f(left + index * step);
  }
  return sum * step / 3;
}

// Fourier convention: f^(omega,k)=int exp(i(omega t-k.x)) f(t,x) dt dx.
// The selected compact bump is even, so only the cosine transform remains.
function bumpFourier(frequency) {
  return simpson((value) => bump(value) * Math.cos(frequency * value), -1, 1, 4096);
}

// For K^{01}=chi and K^{10}=-chi, J^mu=partial_nu K^{nu mu} has
// J^1=partial_t chi.  At the origin the scalar retarded/advanced wave maps are
// int J^1(t-/+|y|,y)/(4 pi |y|) d^3y.
function causalComponent(time, cells, prescription) {
  const step = 2 / cells;
  let sum = 0;
  for (let ix = 0; ix < cells; ix += 1) {
    const x = -1 + (ix + 0.5) * step;
    const bx = bump(x);
    for (let iy = 0; iy < cells; iy += 1) {
      const y = -1 + (iy + 0.5) * step;
      const bxy = bx * bump(y);
      for (let iz = 0; iz < cells; iz += 1) {
        const z = -1 + (iz + 0.5) * step;
        const radius = Math.hypot(x, y, z);
        if (radius === 0) continue;
        const sourceTime = prescription === 'retarded' ? time - radius : time + radius;
        sum += bxy * bump(z) * bumpDerivative(sourceTime) / (4 * Math.PI * radius);
      }
    }
  }
  return sum * step ** 3;
}

function generatedMaxwellSignature() {
  const generated = constructBosonicFieldSystem({ maxTraceDepth: 1 });
  assert(generated.ok, `generator refused the supported grammar: ${JSON.stringify(generated)}`);
  const signature = Object.fromEntries(
    ['R', 'C', 'D', 'wave'].map((name) => [name, polynomialText(generated.fieldSystem[name])]),
  );
  assert(signature.R === 'P', `unexpected generated gauge map: ${signature.R}`);
  assert(signature.C === 'A - 1/2 P T', `unexpected generated defect map: ${signature.C}`);
  assert(signature.D === '-P A + 1/2 P P T + Q', `unexpected generated equation: ${signature.D}`);
  assert(signature.wave === 'Q', `unexpected generated wave completion: ${signature.wave}`);
  return signature;
}

function run() {
  const signature = generatedMaxwellSignature();

  // Spin one has no trace channel.  The generated maps therefore specialize to
  // R=P, C=A, D=Q-PA, which is the Maxwell/Lorenz Green interface.
  const omega = 0.5;
  const transformZero = bumpFourier(0);
  const transformShell = bumpFourier(omega);
  const chiShell = transformShell ** 2 * transformZero ** 2;
  const transverseAmplitude = omega * chiShell;
  assert(transformZero > 0 && transformShell > 0,
    'the compact bump transform should be positive at the selected shell point');
  assert(transverseAmplitude > 0,
    'the generated conserved current should have a nonzero transverse shell amplitude');

  const resolutions = [24, 36, 52];
  const retarded = resolutions.map((cells) => ({
    cells,
    value: causalComponent(2, cells, 'retarded'),
  }));
  const advanced = causalComponent(2, 24, 'advanced');
  assert(retarded.every(({ value }) => value < 0),
    'the retarded witness has the wrong sign or vanished');
  assert(advanced === 0,
    `advanced support should vanish exactly at the selected event, got ${advanced}`);

  const last = retarded.at(-1).value;
  const previous = retarded.at(-2).value;
  const relativeChange = Math.abs(last - previous) / Math.abs(last);
  assert(relativeChange < 0.02,
    `retarded midpoint sequence did not stabilize: relative change ${relativeChange}`);

  console.log(JSON.stringify({
    generated: signature,
    specialization: { spin: 1, R: 'P', C: 'A', D: 'Q - P A', wave: 'Q' },
    compactCurrent: 'K^{01}=chi, K^{10}=-chi, J^mu=partial_nu K^{nu mu}',
    conservationCertificate: 'partial_mu partial_nu K^{nu mu}=0',
    shell: {
      momentum: [omega, 0, 0, omega],
      polarization: 'x',
      bumpTransformZero: transformZero,
      bumpTransformOmega: transformShell,
      transverseAmplitudeMagnitude: transverseAmplitude,
    },
    causal: {
      observation: [2, 0, 0, 0],
      retarded,
      lastRelativeChange: relativeChange,
      advanced,
    },
  }, null, 2));
  console.log('generated compact-source causal-use checks: pass');
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) run();

export { bump, bumpDerivative, bumpFourier, causalComponent };
