/**
 * @license
 * Copyright 2019 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const U = globalThis, z = U.ShadowRoot && (U.ShadyCSS === void 0 || U.ShadyCSS.nativeShadow) && "adoptedStyleSheets" in Document.prototype && "replace" in CSSStyleSheet.prototype, I = Symbol(), W = /* @__PURE__ */ new WeakMap();
let st = class {
  constructor(t, e, s) {
    if (this._$cssResult$ = !0, s !== I) throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");
    this.cssText = t, this.t = e;
  }
  get styleSheet() {
    let t = this.o;
    const e = this.t;
    if (z && t === void 0) {
      const s = e !== void 0 && e.length === 1;
      s && (t = W.get(e)), t === void 0 && ((this.o = t = new CSSStyleSheet()).replaceSync(this.cssText), s && W.set(e, t));
    }
    return t;
  }
  toString() {
    return this.cssText;
  }
};
const ht = (n) => new st(typeof n == "string" ? n : n + "", void 0, I), ct = (n, ...t) => {
  const e = n.length === 1 ? n[0] : t.reduce((s, i, r) => s + ((o) => {
    if (o._$cssResult$ === !0) return o.cssText;
    if (typeof o == "number") return o;
    throw Error("Value passed to 'css' function must be a 'css' function result: " + o + ". Use 'unsafeCSS' to pass non-literal values, but take care to ensure page security.");
  })(i) + n[r + 1], n[0]);
  return new st(e, n, I);
}, lt = (n, t) => {
  if (z) n.adoptedStyleSheets = t.map((e) => e instanceof CSSStyleSheet ? e : e.styleSheet);
  else for (const e of t) {
    const s = document.createElement("style"), i = U.litNonce;
    i !== void 0 && s.setAttribute("nonce", i), s.textContent = e.cssText, n.appendChild(s);
  }
}, V = z ? (n) => n : (n) => n instanceof CSSStyleSheet ? ((t) => {
  let e = "";
  for (const s of t.cssRules) e += s.cssText;
  return ht(e);
})(n) : n;
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const { is: dt, defineProperty: ut, getOwnPropertyDescriptor: pt, getOwnPropertyNames: $t, getOwnPropertySymbols: ft, getPrototypeOf: mt } = Object, O = globalThis, q = O.trustedTypes, _t = q ? q.emptyScript : "", gt = O.reactiveElementPolyfillSupport, w = (n, t) => n, B = { toAttribute(n, t) {
  switch (t) {
    case Boolean:
      n = n ? _t : null;
      break;
    case Object:
    case Array:
      n = n == null ? n : JSON.stringify(n);
  }
  return n;
}, fromAttribute(n, t) {
  let e = n;
  switch (t) {
    case Boolean:
      e = n !== null;
      break;
    case Number:
      e = n === null ? null : Number(n);
      break;
    case Object:
    case Array:
      try {
        e = JSON.parse(n);
      } catch {
        e = null;
      }
  }
  return e;
} }, it = (n, t) => !dt(n, t), K = { attribute: !0, type: String, converter: B, reflect: !1, useDefault: !1, hasChanged: it };
Symbol.metadata ??= Symbol("metadata"), O.litPropertyMetadata ??= /* @__PURE__ */ new WeakMap();
let v = class extends HTMLElement {
  static addInitializer(t) {
    this._$Ei(), (this.l ??= []).push(t);
  }
  static get observedAttributes() {
    return this.finalize(), this._$Eh && [...this._$Eh.keys()];
  }
  static createProperty(t, e = K) {
    if (e.state && (e.attribute = !1), this._$Ei(), this.prototype.hasOwnProperty(t) && ((e = Object.create(e)).wrapped = !0), this.elementProperties.set(t, e), !e.noAccessor) {
      const s = Symbol(), i = this.getPropertyDescriptor(t, s, e);
      i !== void 0 && ut(this.prototype, t, i);
    }
  }
  static getPropertyDescriptor(t, e, s) {
    const { get: i, set: r } = pt(this.prototype, t) ?? { get() {
      return this[e];
    }, set(o) {
      this[e] = o;
    } };
    return { get: i, set(o) {
      const h = i?.call(this);
      r?.call(this, o), this.requestUpdate(t, h, s);
    }, configurable: !0, enumerable: !0 };
  }
  static getPropertyOptions(t) {
    return this.elementProperties.get(t) ?? K;
  }
  static _$Ei() {
    if (this.hasOwnProperty(w("elementProperties"))) return;
    const t = mt(this);
    t.finalize(), t.l !== void 0 && (this.l = [...t.l]), this.elementProperties = new Map(t.elementProperties);
  }
  static finalize() {
    if (this.hasOwnProperty(w("finalized"))) return;
    if (this.finalized = !0, this._$Ei(), this.hasOwnProperty(w("properties"))) {
      const e = this.properties, s = [...$t(e), ...ft(e)];
      for (const i of s) this.createProperty(i, e[i]);
    }
    const t = this[Symbol.metadata];
    if (t !== null) {
      const e = litPropertyMetadata.get(t);
      if (e !== void 0) for (const [s, i] of e) this.elementProperties.set(s, i);
    }
    this._$Eh = /* @__PURE__ */ new Map();
    for (const [e, s] of this.elementProperties) {
      const i = this._$Eu(e, s);
      i !== void 0 && this._$Eh.set(i, e);
    }
    this.elementStyles = this.finalizeStyles(this.styles);
  }
  static finalizeStyles(t) {
    const e = [];
    if (Array.isArray(t)) {
      const s = new Set(t.flat(1 / 0).reverse());
      for (const i of s) e.unshift(V(i));
    } else t !== void 0 && e.push(V(t));
    return e;
  }
  static _$Eu(t, e) {
    const s = e.attribute;
    return s === !1 ? void 0 : typeof s == "string" ? s : typeof t == "string" ? t.toLowerCase() : void 0;
  }
  constructor() {
    super(), this._$Ep = void 0, this.isUpdatePending = !1, this.hasUpdated = !1, this._$Em = null, this._$Ev();
  }
  _$Ev() {
    this._$ES = new Promise((t) => this.enableUpdating = t), this._$AL = /* @__PURE__ */ new Map(), this._$E_(), this.requestUpdate(), this.constructor.l?.forEach((t) => t(this));
  }
  addController(t) {
    (this._$EO ??= /* @__PURE__ */ new Set()).add(t), this.renderRoot !== void 0 && this.isConnected && t.hostConnected?.();
  }
  removeController(t) {
    this._$EO?.delete(t);
  }
  _$E_() {
    const t = /* @__PURE__ */ new Map(), e = this.constructor.elementProperties;
    for (const s of e.keys()) this.hasOwnProperty(s) && (t.set(s, this[s]), delete this[s]);
    t.size > 0 && (this._$Ep = t);
  }
  createRenderRoot() {
    const t = this.shadowRoot ?? this.attachShadow(this.constructor.shadowRootOptions);
    return lt(t, this.constructor.elementStyles), t;
  }
  connectedCallback() {
    this.renderRoot ??= this.createRenderRoot(), this.enableUpdating(!0), this._$EO?.forEach((t) => t.hostConnected?.());
  }
  enableUpdating(t) {
  }
  disconnectedCallback() {
    this._$EO?.forEach((t) => t.hostDisconnected?.());
  }
  attributeChangedCallback(t, e, s) {
    this._$AK(t, s);
  }
  _$ET(t, e) {
    const s = this.constructor.elementProperties.get(t), i = this.constructor._$Eu(t, s);
    if (i !== void 0 && s.reflect === !0) {
      const r = (s.converter?.toAttribute !== void 0 ? s.converter : B).toAttribute(e, s.type);
      this._$Em = t, r == null ? this.removeAttribute(i) : this.setAttribute(i, r), this._$Em = null;
    }
  }
  _$AK(t, e) {
    const s = this.constructor, i = s._$Eh.get(t);
    if (i !== void 0 && this._$Em !== i) {
      const r = s.getPropertyOptions(i), o = typeof r.converter == "function" ? { fromAttribute: r.converter } : r.converter?.fromAttribute !== void 0 ? r.converter : B;
      this._$Em = i;
      const h = o.fromAttribute(e, r.type);
      this[i] = h ?? this._$Ej?.get(i) ?? h, this._$Em = null;
    }
  }
  requestUpdate(t, e, s, i = !1, r) {
    if (t !== void 0) {
      const o = this.constructor;
      if (i === !1 && (r = this[t]), s ??= o.getPropertyOptions(t), !((s.hasChanged ?? it)(r, e) || s.useDefault && s.reflect && r === this._$Ej?.get(t) && !this.hasAttribute(o._$Eu(t, s)))) return;
      this.C(t, e, s);
    }
    this.isUpdatePending === !1 && (this._$ES = this._$EP());
  }
  C(t, e, { useDefault: s, reflect: i, wrapped: r }, o) {
    s && !(this._$Ej ??= /* @__PURE__ */ new Map()).has(t) && (this._$Ej.set(t, o ?? e ?? this[t]), r !== !0 || o !== void 0) || (this._$AL.has(t) || (this.hasUpdated || s || (e = void 0), this._$AL.set(t, e)), i === !0 && this._$Em !== t && (this._$Eq ??= /* @__PURE__ */ new Set()).add(t));
  }
  async _$EP() {
    this.isUpdatePending = !0;
    try {
      await this._$ES;
    } catch (e) {
      Promise.reject(e);
    }
    const t = this.scheduleUpdate();
    return t != null && await t, !this.isUpdatePending;
  }
  scheduleUpdate() {
    return this.performUpdate();
  }
  performUpdate() {
    if (!this.isUpdatePending) return;
    if (!this.hasUpdated) {
      if (this.renderRoot ??= this.createRenderRoot(), this._$Ep) {
        for (const [i, r] of this._$Ep) this[i] = r;
        this._$Ep = void 0;
      }
      const s = this.constructor.elementProperties;
      if (s.size > 0) for (const [i, r] of s) {
        const { wrapped: o } = r, h = this[i];
        o !== !0 || this._$AL.has(i) || h === void 0 || this.C(i, void 0, r, h);
      }
    }
    let t = !1;
    const e = this._$AL;
    try {
      t = this.shouldUpdate(e), t ? (this.willUpdate(e), this._$EO?.forEach((s) => s.hostUpdate?.()), this.update(e)) : this._$EM();
    } catch (s) {
      throw t = !1, this._$EM(), s;
    }
    t && this._$AE(e);
  }
  willUpdate(t) {
  }
  _$AE(t) {
    this._$EO?.forEach((e) => e.hostUpdated?.()), this.hasUpdated || (this.hasUpdated = !0, this.firstUpdated(t)), this.updated(t);
  }
  _$EM() {
    this._$AL = /* @__PURE__ */ new Map(), this.isUpdatePending = !1;
  }
  get updateComplete() {
    return this.getUpdateComplete();
  }
  getUpdateComplete() {
    return this._$ES;
  }
  shouldUpdate(t) {
    return !0;
  }
  update(t) {
    this._$Eq &&= this._$Eq.forEach((e) => this._$ET(e, this[e])), this._$EM();
  }
  updated(t) {
  }
  firstUpdated(t) {
  }
};
v.elementStyles = [], v.shadowRootOptions = { mode: "open" }, v[w("elementProperties")] = /* @__PURE__ */ new Map(), v[w("finalized")] = /* @__PURE__ */ new Map(), gt?.({ ReactiveElement: v }), (O.reactiveElementVersions ??= []).push("2.1.2");
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const D = globalThis, F = (n) => n, M = D.trustedTypes, J = M ? M.createPolicy("lit-html", { createHTML: (n) => n }) : void 0, nt = "$lit$", f = `lit$${Math.random().toFixed(9).slice(2)}$`, rt = "?" + f, yt = `<${rt}>`, g = document, x = () => g.createComment(""), C = (n) => n === null || typeof n != "object" && typeof n != "function", L = Array.isArray, vt = (n) => L(n) || typeof n?.[Symbol.iterator] == "function", H = `[ 	
\f\r]`, E = /<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g, Z = /-->/g, G = />/g, m = RegExp(`>|${H}(?:([^\\s"'>=/]+)(${H}*=${H}*(?:[^ 	
\f\r"'\`<>=]|("|')|))|$)`, "g"), Q = /'/g, X = /"/g, ot = /^(?:script|style|textarea|title)$/i, At = (n) => (t, ...e) => ({ _$litType$: n, strings: t, values: e }), y = At(1), A = Symbol.for("lit-noChange"), d = Symbol.for("lit-nothing"), Y = /* @__PURE__ */ new WeakMap(), _ = g.createTreeWalker(g, 129);
function at(n, t) {
  if (!L(n) || !n.hasOwnProperty("raw")) throw Error("invalid template strings array");
  return J !== void 0 ? J.createHTML(t) : t;
}
const bt = (n, t) => {
  const e = n.length - 1, s = [];
  let i, r = t === 2 ? "<svg>" : t === 3 ? "<math>" : "", o = E;
  for (let h = 0; h < e; h++) {
    const a = n[h];
    let c, u, l = -1, p = 0;
    for (; p < a.length && (o.lastIndex = p, u = o.exec(a), u !== null); ) p = o.lastIndex, o === E ? u[1] === "!--" ? o = Z : u[1] !== void 0 ? o = G : u[2] !== void 0 ? (ot.test(u[2]) && (i = RegExp("</" + u[2], "g")), o = m) : u[3] !== void 0 && (o = m) : o === m ? u[0] === ">" ? (o = i ?? E, l = -1) : u[1] === void 0 ? l = -2 : (l = o.lastIndex - u[2].length, c = u[1], o = u[3] === void 0 ? m : u[3] === '"' ? X : Q) : o === X || o === Q ? o = m : o === Z || o === G ? o = E : (o = m, i = void 0);
    const $ = o === m && n[h + 1].startsWith("/>") ? " " : "";
    r += o === E ? a + yt : l >= 0 ? (s.push(c), a.slice(0, l) + nt + a.slice(l) + f + $) : a + f + (l === -2 ? h : $);
  }
  return [at(n, r + (n[e] || "<?>") + (t === 2 ? "</svg>" : t === 3 ? "</math>" : "")), s];
};
class P {
  constructor({ strings: t, _$litType$: e }, s) {
    let i;
    this.parts = [];
    let r = 0, o = 0;
    const h = t.length - 1, a = this.parts, [c, u] = bt(t, e);
    if (this.el = P.createElement(c, s), _.currentNode = this.el.content, e === 2 || e === 3) {
      const l = this.el.content.firstChild;
      l.replaceWith(...l.childNodes);
    }
    for (; (i = _.nextNode()) !== null && a.length < h; ) {
      if (i.nodeType === 1) {
        if (i.hasAttributes()) for (const l of i.getAttributeNames()) if (l.endsWith(nt)) {
          const p = u[o++], $ = i.getAttribute(l).split(f), N = /([.?@])?(.*)/.exec(p);
          a.push({ type: 1, index: r, name: N[2], strings: $, ctor: N[1] === "." ? wt : N[1] === "?" ? St : N[1] === "@" ? xt : R }), i.removeAttribute(l);
        } else l.startsWith(f) && (a.push({ type: 6, index: r }), i.removeAttribute(l));
        if (ot.test(i.tagName)) {
          const l = i.textContent.split(f), p = l.length - 1;
          if (p > 0) {
            i.textContent = M ? M.emptyScript : "";
            for (let $ = 0; $ < p; $++) i.append(l[$], x()), _.nextNode(), a.push({ type: 2, index: ++r });
            i.append(l[p], x());
          }
        }
      } else if (i.nodeType === 8) if (i.data === rt) a.push({ type: 2, index: r });
      else {
        let l = -1;
        for (; (l = i.data.indexOf(f, l + 1)) !== -1; ) a.push({ type: 7, index: r }), l += f.length - 1;
      }
      r++;
    }
  }
  static createElement(t, e) {
    const s = g.createElement("template");
    return s.innerHTML = t, s;
  }
}
function b(n, t, e = n, s) {
  if (t === A) return t;
  let i = s !== void 0 ? e._$Co?.[s] : e._$Cl;
  const r = C(t) ? void 0 : t._$litDirective$;
  return i?.constructor !== r && (i?._$AO?.(!1), r === void 0 ? i = void 0 : (i = new r(n), i._$AT(n, e, s)), s !== void 0 ? (e._$Co ??= [])[s] = i : e._$Cl = i), i !== void 0 && (t = b(n, i._$AS(n, t.values), i, s)), t;
}
class Et {
  constructor(t, e) {
    this._$AV = [], this._$AN = void 0, this._$AD = t, this._$AM = e;
  }
  get parentNode() {
    return this._$AM.parentNode;
  }
  get _$AU() {
    return this._$AM._$AU;
  }
  u(t) {
    const { el: { content: e }, parts: s } = this._$AD, i = (t?.creationScope ?? g).importNode(e, !0);
    _.currentNode = i;
    let r = _.nextNode(), o = 0, h = 0, a = s[0];
    for (; a !== void 0; ) {
      if (o === a.index) {
        let c;
        a.type === 2 ? c = new k(r, r.nextSibling, this, t) : a.type === 1 ? c = new a.ctor(r, a.name, a.strings, this, t) : a.type === 6 && (c = new Ct(r, this, t)), this._$AV.push(c), a = s[++h];
      }
      o !== a?.index && (r = _.nextNode(), o++);
    }
    return _.currentNode = g, i;
  }
  p(t) {
    let e = 0;
    for (const s of this._$AV) s !== void 0 && (s.strings !== void 0 ? (s._$AI(t, s, e), e += s.strings.length - 2) : s._$AI(t[e])), e++;
  }
}
class k {
  get _$AU() {
    return this._$AM?._$AU ?? this._$Cv;
  }
  constructor(t, e, s, i) {
    this.type = 2, this._$AH = d, this._$AN = void 0, this._$AA = t, this._$AB = e, this._$AM = s, this.options = i, this._$Cv = i?.isConnected ?? !0;
  }
  get parentNode() {
    let t = this._$AA.parentNode;
    const e = this._$AM;
    return e !== void 0 && t?.nodeType === 11 && (t = e.parentNode), t;
  }
  get startNode() {
    return this._$AA;
  }
  get endNode() {
    return this._$AB;
  }
  _$AI(t, e = this) {
    t = b(this, t, e), C(t) ? t === d || t == null || t === "" ? (this._$AH !== d && this._$AR(), this._$AH = d) : t !== this._$AH && t !== A && this._(t) : t._$litType$ !== void 0 ? this.$(t) : t.nodeType !== void 0 ? this.T(t) : vt(t) ? this.k(t) : this._(t);
  }
  O(t) {
    return this._$AA.parentNode.insertBefore(t, this._$AB);
  }
  T(t) {
    this._$AH !== t && (this._$AR(), this._$AH = this.O(t));
  }
  _(t) {
    this._$AH !== d && C(this._$AH) ? this._$AA.nextSibling.data = t : this.T(g.createTextNode(t)), this._$AH = t;
  }
  $(t) {
    const { values: e, _$litType$: s } = t, i = typeof s == "number" ? this._$AC(t) : (s.el === void 0 && (s.el = P.createElement(at(s.h, s.h[0]), this.options)), s);
    if (this._$AH?._$AD === i) this._$AH.p(e);
    else {
      const r = new Et(i, this), o = r.u(this.options);
      r.p(e), this.T(o), this._$AH = r;
    }
  }
  _$AC(t) {
    let e = Y.get(t.strings);
    return e === void 0 && Y.set(t.strings, e = new P(t)), e;
  }
  k(t) {
    L(this._$AH) || (this._$AH = [], this._$AR());
    const e = this._$AH;
    let s, i = 0;
    for (const r of t) i === e.length ? e.push(s = new k(this.O(x()), this.O(x()), this, this.options)) : s = e[i], s._$AI(r), i++;
    i < e.length && (this._$AR(s && s._$AB.nextSibling, i), e.length = i);
  }
  _$AR(t = this._$AA.nextSibling, e) {
    for (this._$AP?.(!1, !0, e); t !== this._$AB; ) {
      const s = F(t).nextSibling;
      F(t).remove(), t = s;
    }
  }
  setConnected(t) {
    this._$AM === void 0 && (this._$Cv = t, this._$AP?.(t));
  }
}
class R {
  get tagName() {
    return this.element.tagName;
  }
  get _$AU() {
    return this._$AM._$AU;
  }
  constructor(t, e, s, i, r) {
    this.type = 1, this._$AH = d, this._$AN = void 0, this.element = t, this.name = e, this._$AM = i, this.options = r, s.length > 2 || s[0] !== "" || s[1] !== "" ? (this._$AH = Array(s.length - 1).fill(new String()), this.strings = s) : this._$AH = d;
  }
  _$AI(t, e = this, s, i) {
    const r = this.strings;
    let o = !1;
    if (r === void 0) t = b(this, t, e, 0), o = !C(t) || t !== this._$AH && t !== A, o && (this._$AH = t);
    else {
      const h = t;
      let a, c;
      for (t = r[0], a = 0; a < r.length - 1; a++) c = b(this, h[s + a], e, a), c === A && (c = this._$AH[a]), o ||= !C(c) || c !== this._$AH[a], c === d ? t = d : t !== d && (t += (c ?? "") + r[a + 1]), this._$AH[a] = c;
    }
    o && !i && this.j(t);
  }
  j(t) {
    t === d ? this.element.removeAttribute(this.name) : this.element.setAttribute(this.name, t ?? "");
  }
}
class wt extends R {
  constructor() {
    super(...arguments), this.type = 3;
  }
  j(t) {
    this.element[this.name] = t === d ? void 0 : t;
  }
}
class St extends R {
  constructor() {
    super(...arguments), this.type = 4;
  }
  j(t) {
    this.element.toggleAttribute(this.name, !!t && t !== d);
  }
}
class xt extends R {
  constructor(t, e, s, i, r) {
    super(t, e, s, i, r), this.type = 5;
  }
  _$AI(t, e = this) {
    if ((t = b(this, t, e, 0) ?? d) === A) return;
    const s = this._$AH, i = t === d && s !== d || t.capture !== s.capture || t.once !== s.once || t.passive !== s.passive, r = t !== d && (s === d || i);
    i && this.element.removeEventListener(this.name, this, s), r && this.element.addEventListener(this.name, this, t), this._$AH = t;
  }
  handleEvent(t) {
    typeof this._$AH == "function" ? this._$AH.call(this.options?.host ?? this.element, t) : this._$AH.handleEvent(t);
  }
}
class Ct {
  constructor(t, e, s) {
    this.element = t, this.type = 6, this._$AN = void 0, this._$AM = e, this.options = s;
  }
  get _$AU() {
    return this._$AM._$AU;
  }
  _$AI(t) {
    b(this, t);
  }
}
const Pt = D.litHtmlPolyfillSupport;
Pt?.(P, k), (D.litHtmlVersions ??= []).push("3.3.3");
const kt = (n, t, e) => {
  const s = e?.renderBefore ?? t;
  let i = s._$litPart$;
  if (i === void 0) {
    const r = e?.renderBefore ?? null;
    s._$litPart$ = i = new k(t.insertBefore(x(), r), r, void 0, e ?? {});
  }
  return i._$AI(n), i;
};
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const j = globalThis;
class S extends v {
  constructor() {
    super(...arguments), this.renderOptions = { host: this }, this._$Do = void 0;
  }
  createRenderRoot() {
    const t = super.createRenderRoot();
    return this.renderOptions.renderBefore ??= t.firstChild, t;
  }
  update(t) {
    const e = this.render();
    this.hasUpdated || (this.renderOptions.isConnected = this.isConnected), super.update(t), this._$Do = kt(e, this.renderRoot, this.renderOptions);
  }
  connectedCallback() {
    super.connectedCallback(), this._$Do?.setConnected(!0);
  }
  disconnectedCallback() {
    super.disconnectedCallback(), this._$Do?.setConnected(!1);
  }
  render() {
    return A;
  }
}
S._$litElement$ = !0, S.finalized = !0, j.litElementHydrateSupport?.({ LitElement: S });
const Nt = j.litElementPolyfillSupport;
Nt?.({ LitElement: S });
(j.litElementVersions ??= []).push("4.2.2");
const Ut = {
  title: "AmberChest",
  noAccounts: "No mailbox found. Is the AmberChest integration set up?",
  messages: "Messages",
  size: "Size",
  lastBackup: "Last backup",
  never: "never",
  running: "backing up",
  backUpNow: "Back up now",
  nextRun: "Next run",
  total: "Archive"
}, Mt = {
  title: "AmberChest",
  noAccounts: "Kein Postfach gefunden. Ist die AmberChest-Integration eingerichtet?",
  messages: "Nachrichten",
  size: "Größe",
  lastBackup: "Letzte Sicherung",
  never: "nie",
  running: "sichert gerade",
  backUpNow: "Jetzt sichern",
  nextRun: "Nächster Lauf",
  total: "Archiv"
};
function Ot(n) {
  return (n ?? "en").split("-")[0] === "de" ? Mt : Ut;
}
const T = "amberchest";
function tt(n) {
  if (n === null) return "–";
  if (n < 1024) return `${n} B`;
  const t = ["KB", "MB", "GB", "TB"];
  let e = n / 1024, s = 0;
  for (; e >= 1024 && s < t.length - 1; )
    e /= 1024, s += 1;
  return `${e.toFixed(e < 10 ? 1 : 0)} ${t[s]}`;
}
function et(n, t, e) {
  if (!n) return e;
  const s = new Date(n).getTime();
  if (Number.isNaN(s)) return e;
  const i = Math.round((s - Date.now()) / 1e3), r = new Intl.RelativeTimeFormat(t, { numeric: "auto" }), o = [
    ["second", 60],
    ["minute", 60],
    ["hour", 24],
    ["day", 30],
    ["month", 12]
  ];
  let h = i;
  for (const [a, c] of o) {
    if (Math.abs(h) < c) return r.format(Math.round(h), a);
    h /= c;
  }
  return r.format(Math.round(h), "year");
}
class Rt extends S {
  static {
    this.properties = {
      hass: { attribute: !1 },
      _config: { state: !0 }
    };
  }
  static {
    this.styles = ct`
    ha-card {
      padding: 12px 0 4px;
    }
    .head {
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 4px 16px 10px;
    }
    .head .name {
      font-size: 1.15rem;
      font-weight: 500;
      color: var(--primary-text-color);
    }
    .head .total {
      margin-left: auto;
      font-size: 0.85rem;
      color: var(--secondary-text-color);
      text-align: right;
    }
    .row {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 10px 16px;
      border-top: 1px solid var(--divider-color);
    }
    .row .label {
      min-width: 0;
      flex: 1;
    }
    .row .name {
      color: var(--primary-text-color);
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
    .row .meta {
      font-size: 0.8rem;
      color: var(--secondary-text-color);
    }
    .numbers {
      text-align: right;
      font-size: 0.8rem;
      color: var(--secondary-text-color);
      white-space: nowrap;
    }
    .numbers strong {
      display: block;
      font-size: 0.95rem;
      font-weight: 500;
      color: var(--primary-text-color);
    }
    button {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      border: 1px solid var(--divider-color);
      border-radius: 18px;
      background: none;
      color: var(--primary-color);
      font: inherit;
      font-size: 0.8rem;
      padding: 6px 12px;
      cursor: pointer;
    }
    button:disabled {
      color: var(--secondary-text-color);
      cursor: default;
    }
    .empty {
      padding: 8px 16px 16px;
      color: var(--secondary-text-color);
    }
    .spin {
      animation: spin 1.4s linear infinite;
    }
    @keyframes spin {
      to {
        transform: rotate(360deg);
      }
    }
  `;
  }
  setConfig(t) {
    this._config = t;
  }
  getCardSize() {
    return 1 + this._mailboxes().length;
  }
  static getStubConfig() {
    return { type: `custom:${T}-card` };
  }
  /** Collects the entities of the integration and groups them by device. */
  _mailboxes() {
    const t = this.hass;
    if (!t?.entities || !t.devices) return [];
    const e = /* @__PURE__ */ new Map();
    for (const [s, i] of Object.entries(t.entities)) {
      if (i.platform !== T || !i.device_id) continue;
      const r = t.states[s];
      if (!r) continue;
      const o = s.split(".")[1] ?? "", h = t.devices[i.device_id];
      if (!h) continue;
      let a = e.get(i.device_id);
      a || (a = {
        deviceId: i.device_id,
        name: h.name_by_user || h.name || o,
        messages: null,
        bytes: null,
        lastBackup: null,
        running: !1,
        phase: null,
        backupButton: null
      }, e.set(i.device_id, a));
      const c = String(r.attributes.device_class ?? ""), u = String(r.attributes.unit_of_measurement ?? "");
      s.startsWith("binary_sensor.") ? (a.running = r.state === "on", a.phase = r.attributes.phase ?? null) : s.startsWith("button.") ? a.backupButton === null && (a.backupButton = s) : c === "data_size" ? a.bytes = Number(r.state) * (u === "MB" ? 1024 * 1024 : 1) : c === "timestamp" ? a.lastBackup = r.state === "unknown" ? null : r.state : u === "messages" && (a.messages = Number(r.state));
    }
    return [...e.values()].filter((s) => s.messages !== null).sort((s, i) => s.name.localeCompare(i.name));
  }
  _totals() {
    const t = this.hass;
    let e = 0, s = null;
    if (!t?.entities) return { bytes: e, nextRun: s };
    for (const [i, r] of Object.entries(t.entities)) {
      if (r.platform !== T) continue;
      const o = t.states[i];
      if (!o) continue;
      if (typeof o.attributes.accounts == "number") {
        const a = String(o.attributes.unit_of_measurement ?? "");
        e = Number(o.state) * (a === "MB" ? 1024 * 1024 : 1);
      }
      o.attributes.cron !== void 0 && o.state !== "unknown" && (s = o.state);
    }
    return { bytes: e, nextRun: s };
  }
  async _backup(t) {
    await this.hass?.callService("button", "press", { entity_id: t });
  }
  render() {
    const t = this.hass;
    if (!t || !this._config) return d;
    const e = Ot(t.language), s = t.language ?? "en", i = this._mailboxes().filter(
      (o) => !this._config?.hide_empty || (o.messages ?? 0) > 0
    ), r = this._totals();
    return y`
      <ha-card>
        <div class="head">
          <ha-icon icon="mdi:email-sync-outline"></ha-icon>
          <span class="name">${this._config.title ?? e.title}</span>
          <span class="total">
            ${e.total}: ${tt(r.bytes)}
            ${r.nextRun ? y`<br />${e.nextRun}: ${et(r.nextRun, s, e.never)}` : d}
          </span>
        </div>

        ${i.length === 0 ? y`<div class="empty">${e.noAccounts}</div>` : i.map(
      (o) => y`
                <div class="row">
                  <div class="label">
                    <div class="name">${o.name}</div>
                    <div class="meta">
                      ${o.running ? y`<ha-icon class="spin" icon="mdi:loading" style="--mdc-icon-size:14px"></ha-icon>
                            ${e.running}${o.phase ? ` · ${o.phase}` : ""}` : y`${e.lastBackup}: ${et(o.lastBackup, s, e.never)}`}
                    </div>
                  </div>
                  <div class="numbers">
                    <strong>${(o.messages ?? 0).toLocaleString(s)}</strong>
                    ${tt(o.bytes)}
                  </div>
                  <button
                    ?disabled=${o.running || !o.backupButton}
                    @click=${() => o.backupButton && this._backup(o.backupButton)}
                  >
                    <ha-icon icon="mdi:cloud-download" style="--mdc-icon-size:16px"></ha-icon>
                    ${e.backUpNow}
                  </button>
                </div>
              `
    )}
      </ha-card>
    `;
  }
}
customElements.define("amberchest-card", Rt);
const Ht = window.customCards ??= [];
Ht.push({
  type: "amberchest-card",
  name: "AmberChest",
  description: "Every archived mailbox with its numbers and a backup button.",
  preview: !0
});
export {
  Rt as AmberChestCard
};
