"use strict";
(self.webpackChunk_N_E = self.webpackChunk_N_E || []).push([[5932], {
    61806: function(e, t, r) {
        r.d(t, {
            default: function() {
                return s
            }
        });
        var a = r(57437)
          , n = r(2265)
          , o = r(99376);
        function s() {
            let e = (0,
            o.usePathname)()
              , [t,r] = (0,
            n.useState)(!1);
            return ((0,
            n.useEffect)( () => {
                r(!0)
            }
            , []),
            (0,
            n.useEffect)( () => {
                t && ( () => {
                    try {
                        if (window.ezstandalone && window.ezstandalone.cmd)
                            window.ezstandalone.cmd.push(function() {
                                try {
                                    window.ezstandalone.showAds(113)
                                } catch (e) {
                                    console.error("Ads102: Error calling showAds:", e)
                                }
                            });
                        else {
                            let e = setInterval( () => {
                                try {
                                    window.ezstandalone && window.ezstandalone.cmd && (window.ezstandalone.cmd.push(function() {
                                        try {
                                            window.ezstandalone.showAds(113)
                                        } catch (e) {
                                            console.error("Ads102: Error calling showAds in interval:", e)
                                        }
                                    }),
                                    clearInterval(e))
                                } catch (t) {
                                    console.error("Ads102: Error in interval check:", t),
                                    clearInterval(e)
                                }
                            }
                            , 100);
                            setTimeout( () => {
                                clearInterval(e)
                            }
                            , 1e4)
                        }
                    } catch (e) {
                        console.error("Ads102: Error in showAds function:", e)
                    }
                }
                )()
            }
            , [e, t]),
            t) ? (0,
            a.jsx)(a.Fragment, {
                children: (0,
                a.jsx)("div", {
                    className: "w-full mx-auto",
                    children: (0,
                    a.jsx)("div", {
                        id: "ezoic-pub-ad-placeholder-113"
                    })
                })
            }) : null
        }
    },
    6696: function(e, t, r) {
        r.d(t, {
            Z: function() {
                return s
            }
        });
        var a = r(57437)
          , n = r(2265)
          , o = r(33145);
        function s(e) {
            let {setAspectRatio: t, match_input_image: r=!1, style: s="default"} = e
              , i = [{
                aspect: "match_input_image",
                display: "Match input image",
                width: 1248,
                height: 1248,
                icon: "none"
            }, {
                aspect: "1:1",
                display: "1:1",
                width: 1248,
                height: 1248,
                icon: "1_1"
            }, {
                aspect: "1:2",
                display: "1:2",
                width: 624,
                height: 1248,
                icon: "1_2"
            }, {
                aspect: "2:1",
                display: "2:1",
                width: 1248,
                height: 624,
                icon: "2_1"
            }, {
                aspect: "2:3",
                display: "2:3",
                width: 832,
                height: 1248,
                icon: "2_3"
            }, {
                aspect: "3:2",
                display: "3:2",
                width: 1248,
                height: 832,
                icon: "3_2"
            }, {
                aspect: "9:16",
                display: "9:16",
                width: 702,
                height: 1248,
                icon: "9_16"
            }, {
                aspect: "16:9",
                display: "16:9",
                width: 1248,
                height: 702,
                icon: "16_9"
            }]
              , d = r ? i : i.filter(e => "match_input_image" !== e.aspect)
              , [c,l] = (0,
            n.useState)(d[0])
              , h = e => {
                l(d[e]),
                r ? t(t => ({
                    ...t,
                    width: d[e].width,
                    height: d[e].height,
                    aspect: d[e].aspect
                })) : t(t => ({
                    ...t,
                    width: d[e].width,
                    height: d[e].height,
                    aspect: d[e].aspect
                }))
            }
              , u = (0,
            a.jsxs)("div", {
                children: [(0,
                a.jsx)("label", {
                    className: "pl-1 text-left text-sm font-semibold block mb-2",
                    children: "Aspect Ratio"
                }), (0,
                a.jsxs)("div", {
                    className: "hs-dropdown w-full relative inline-flex",
                    children: [(0,
                    a.jsxs)("button", {
                        id: "hs-dropdown-default",
                        type: "button",
                        className: "hs-dropdown-toggle w-full py-2 px-3 inline-flex items-center justify-between text-sm font-medium rounded-lg border border-gray-200 bg-white text-gray-800 shadow-sm hover:bg-gray-50 focus:outline-none focus:bg-gray-50 disabled:opacity-50 disabled:pointer-events-none dark:bg-neutral-800 dark:border-neutral-700 dark:text-white dark:hover:bg-neutral-700 dark:focus:bg-neutral-700",
                        "aria-haspopup": "menu",
                        "aria-expanded": "false",
                        "aria-label": "Dropdown",
                        children: [c.display, (0,
                        a.jsx)("svg", {
                            className: "hs-dropdown-open:rotate-180 size-4",
                            xmlns: "http://www.w3.org/2000/svg",
                            width: "24",
                            height: "24",
                            viewBox: "0 0 24 24",
                            fill: "none",
                            stroke: "currentColor",
                            strokeWidth: "2",
                            strokeLinecap: "round",
                            strokeLinejoin: "round",
                            children: (0,
                            a.jsx)("path", {
                                d: "m6 9 6 6 6-6"
                            })
                        })]
                    }), (0,
                    a.jsx)("div", {
                        className: "hs-dropdown-menu transition-[opacity,margin] duration border hs-dropdown-open:opacity-100 opacity-0 hidden min-w-60 bg-white shadow-md rounded-lg mt-2 dark:bg-neutral-800 dark:border dark:border-neutral-700 dark:divide-neutral-700 after:h-4 after:absolute after:-bottom-4 after:start-0 after:w-full before:h-4 before:absolute before:-top-4 before:start-0 before:w-full",
                        role: "menu",
                        "aria-orientation": "vertical",
                        "aria-labelledby": "hs-dropdown-default",
                        children: (0,
                        a.jsx)("div", {
                            className: "p-1 space-y-0.5",
                            children: d.map( (e, t) => (0,
                            a.jsxs)("div", {
                                className: "flex items-center gap-x-3.5 py-2 px-3 rounded-lg text-sm text-gray-800 hover:bg-gray-100 focus:outline-none focus:bg-gray-100 dark:text-neutral-400 dark:hover:bg-neutral-700 dark:hover:text-neutral-300 dark:focus:bg-neutral-700",
                                onClick: () => h(t),
                                children: ["none" !== e.icon && (0,
                                a.jsx)(o.default, {
                                    width: 18,
                                    height: 18,
                                    className: "text-neutral-700 dark:text-white",
                                    src: "/images/icons/aspects/".concat(e.icon, ".svg"),
                                    alt: e.display
                                }), (0,
                                a.jsx)("h3", {
                                    className: "text-sm",
                                    children: e.display
                                })]
                            }, t))
                        })
                    })]
                })]
            })
              , p = (0,
            a.jsxs)("div", {
                className: "flex flex-row justify-between items-center",
                children: [(0,
                a.jsx)("label", {
                    className: "pl-1 text-left text-sm font-semibold block",
                    children: "Aspect Ratio"
                }), (0,
                a.jsxs)("div", {
                    className: "m-1 hs-dropdown [--trigger:hover] relative inline-flex items-center",
                    children: [(0,
                    a.jsx)("span", {
                        className: "text-sm mr-2 text-right",
                        children: c.display
                    }), (0,
                    a.jsx)("button", {
                        id: "hs-dropdown-hover-event",
                        type: "button",
                        className: "hs-dropdown-toggle p-1 bg-white shadow-sm dark:bg-neutral-900 rounded-full",
                        "aria-haspopup": "menu",
                        "aria-expanded": "false",
                        "aria-label": "Dropdown",
                        children: (0,
                        a.jsx)("svg", {
                            className: "hs-dropdown-open:rotate-180 size-4",
                            xmlns: "http://www.w3.org/2000/svg",
                            width: "24",
                            height: "24",
                            viewBox: "0 0 24 24",
                            fill: "none",
                            stroke: "currentColor",
                            strokeWidth: "2",
                            strokeLinecap: "round",
                            strokeLinejoin: "round",
                            children: (0,
                            a.jsx)("path", {
                                d: "m6 9 6 6 6-6"
                            })
                        })
                    }), (0,
                    a.jsx)("div", {
                        className: "hs-dropdown-menu transition-[opacity,margin] duration hs-dropdown-open:opacity-100 opacity-0 hidden min-w-60 max-h-60 bg-white shadow-md rounded-lg mt-2 dark:bg-neutral-800 dark:border dark:border-neutral-700 dark:divide-neutral-700 after:h-4 after:absolute after:-bottom-4 after:start-0 after:w-full before:h-4 before:absolute before:-top-4 before:start-0 before:w-full z-10",
                        role: "menu",
                        "aria-orientation": "vertical",
                        "aria-labelledby": "hs-dropdown-hover-event",
                        children: (0,
                        a.jsx)("div", {
                            className: "p-1 space-y-0.5 max-h-60 overflow-y-scroll",
                            children: d.map( (e, t) => (0,
                            a.jsxs)("div", {
                                className: "flex items-center gap-x-3.5 py-2 px-3 rounded-lg text-sm text-gray-800 hover:bg-gray-100 focus:outline-none focus:bg-gray-100 dark:text-neutral-400 dark:hover:bg-neutral-700 dark:hover:text-neutral-300 dark:focus:bg-neutral-700",
                                onClick: () => h(t),
                                children: ["none" !== e.icon && (0,
                                a.jsx)(o.default, {
                                    width: 18,
                                    height: 18,
                                    className: "text-neutral-700 dark:text-white",
                                    src: "/images/icons/aspects/".concat(e.icon, ".svg"),
                                    alt: e.display
                                }), (0,
                                a.jsx)("h3", {
                                    className: "text-sm",
                                    children: e.display
                                })]
                            }, t))
                        })
                    })]
                })]
            });
            return (0,
            a.jsxs)(a.Fragment, {
                children: ["default" === s && u, "icon" === s && p]
            })
        }
    },
    30365: function(e, t, r) {
        r.d(t, {
            Bf: function() {
                return i
            },
            Dw: function() {
                return n
            },
            f_: function() {
                return o
            },
            rt: function() {
                return s
            }
        }),
        r(83079);
        var a = r(12119);
        (0,
        a.$)("68c5f9b201405d9e1343f3e570f6b6c786df16ae"),
        (0,
        a.$)("906d4a7d1f708e4e261d401b56d18a9373c5ebd3");
        var n = (0,
        a.$)("1eeefc61e5469e1a173b48743a3cb8dd77eed91b")
          , o = (0,
        a.$)("d11c5dc09ea51cc153a48d085ac295f01fd51c5b");
        (0,
        a.$)("a136cfc4b7149fec24faabc4f005c630b1d4f83c"),
        (0,
        a.$)("41e3c9488bc2af24c171afd02f9822b680bb0f61"),
        (0,
        a.$)("0cd7fb6a0ea6df1ab1d55bb7720d7477a288e36a"),
        (0,
        a.$)("36a9ef943345cc114865dfa3464c46ad238675ff"),
        (0,
        a.$)("9a901b55fbe9ec31ff56791735fbd6c83e7bd1b3");
        var s = (0,
        a.$)("992f4d8f31abf6117af57c34e1c0c4d87cd48edc")
          , i = (0,
        a.$)("eff46f89aef87f4fa6869531d03140ed30014edc")
    },
    35594: function(e, t, r) {
        var a = r(83464);
        let n = null;
        t.Z = function(e) {
            return new Promise( (t, r) => {
                (n || (n = function() {
                    let e = a.Z.create({
                        baseURL: "https://access.vheer.com",
                        timeout: 3e5
                    });
                    return e.interceptors.request.use(e => e, e => Promise.reject(e)),
                    e.interceptors.response.use(e => {
                        let {data: t, status: r} = e
                          , {code: a, data: n, message: o} = t;
                        return 200 == a ? n : Promise.reject(t)
                    }
                    , async e => {
                        if ("ECONNABORTED" === e.code && -1 !== e.message.indexOf("timeout"))
                            ;
                        else {
                            let {status: t, data: r, config: a} = e.response;
                            500 === t ? notification.error({
                                message: "服务器错误",
                                description: r.message || "未知错误"
                            }) : 413 === t ? notification.error({
                                message: "文件过大",
                                description: "文件过大，选个小点的吧~"
                            }) : 404 === t ? notification.error({
                                message: "请求资源不存在",
                                description: "请求的资源不存在，请检查接口地址"
                            }) : 400 === t && notification.error({
                                message: "客户端错误",
                                description: Array.isArray(r.message) ? r.message.join("；") : r.message || "未知错误"
                            })
                        }
                        return Promise.reject(e)
                    }
                    ),
                    e
                }(void 0)),
                n).request(e).then(r => {
                    var a;
                    (null === (a = e.interceptors) || void 0 === a ? void 0 : a.responseInterceptors) && (r = e.interceptors.responseInterceptors(r)),
                    t(r)
                }
                ).catch(e => {
                    r({
                        code: e.code,
                        data: e.data,
                        message: e.msg
                    })
                }
                )
            }
            )
        }
    },
    32577: function(e, t) {
        class r {
            async deriveKey(e) {
                let t = new TextEncoder
                  , r = await window.crypto.subtle.importKey("raw", t.encode(e), {
                    name: "PBKDF2"
                }, !1, ["deriveKey"]);
                return await window.crypto.subtle.deriveKey({
                    name: "PBKDF2",
                    salt: t.encode("vheer-salt-2024"),
                    iterations: 1e5,
                    hash: "SHA-256"
                }, r, {
                    name: "AES-GCM",
                    length: 256
                }, !1, ["encrypt", "decrypt"])
            }
            async encrypt(e) {
                try {
                    let t = await this.key
                      , r = new TextEncoder
                      , a = window.crypto.getRandomValues(new Uint8Array(12))
                      , n = await window.crypto.subtle.encrypt({
                        name: "AES-GCM",
                        iv: a
                    }, t, r.encode(e))
                      , o = new Uint8Array(a.length + n.byteLength);
                    return o.set(a),
                    o.set(new Uint8Array(n), a.length),
                    btoa(String.fromCharCode(...o))
                } catch (e) {
                    throw console.error("Encryption error:", e),
                    Error("Failed to encrypt data")
                }
            }
            async decrypt(e) {
                try {
                    let t = await this.key
                      , r = new TextDecoder
                      , a = new Uint8Array(atob(e).split("").map(e => e.charCodeAt(0)))
                      , n = a.slice(0, 12)
                      , o = a.slice(12)
                      , s = await window.crypto.subtle.decrypt({
                        name: "AES-GCM",
                        iv: n
                    }, t, o);
                    return r.decode(s)
                } catch (e) {
                    throw console.error("Decryption error:", e),
                    Error("Failed to decrypt data")
                }
            }
            async decryptAndLog(e) {
                let t = arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : "Data";
                try {
                    let t = await this.decrypt(e);
                    return JSON.parse(t)
                } catch (e) {
                    return console.error("❌ ".concat(t, " decryption failed:"), e),
                    null
                }
            }
            constructor() {
                this.encryptionKey = "vH33r_2025_AES_GCM_S3cur3_K3y_9X7mP4qR8nT2wE5yU1oI6aS3dF7gH0jK9lZ",
                this.key = this.deriveKey(this.encryptionKey)
            }
        }
        let a = new r;
        t.Z = a
    }
}]);
