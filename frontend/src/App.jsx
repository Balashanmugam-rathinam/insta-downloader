import { useState, useRef } from "react";

const BASE_URL = "insta-downloader-production-a2d6.up.railway.app";

function GlowOrb({ className }) {
  return (
    <div
      className={`absolute rounded-full blur-[120px] opacity-20 pointer-events-none ${className}`}
    />
  );
}

function InstagramIcon() {
  return (
    <svg
      width="18"
      height="18"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.5"
    >
      <rect x="2" y="2" width="20" height="20" rx="5" />
      <circle cx="12" cy="12" r="4" />
    </svg>
  );
}

function DownloadIcon({ size = 18 }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.5"
    >
      <path d="M12 3v13M7 11l5 5 5-5" />
      <path d="M3 19h18" />
    </svg>
  );
}

function Spinner() {
  return (
    <div className="w-12 h-12 border border-white/10 border-t-white rounded-full animate-spin" />
  );
}

function SuccessRing() {
  return (
    <div className="w-16 h-16 rounded-full border border-green-400/30 flex items-center justify-center">
      <svg
        width="28"
        height="28"
        viewBox="0 0 24 24"
        fill="none"
        stroke="#4ade80"
        strokeWidth="1.5"
      >
        <path d="M5 13l4 4L19 7" />
      </svg>
    </div>
  );
}

export default function App() {

  const [url, setUrl] = useState("");
  const [status, setStatus] = useState("idle");
  const [downloadUrl, setDownloadUrl] = useState("");
  const [errorMsg, setErrorMsg] = useState("");
  const [title, setTitle] = useState("");
  const [thumbnail, setThumbnail] = useState("");
  const [progress, setProgress] = useState(0);
  const [pasted, setPasted] = useState(false);

  const inputRef = useRef(null);

  const isValidUrl = url.trim().length > 10;

 const handlePaste = async () => {

  try {

    if (navigator.clipboard) {

      const text = await navigator.clipboard.readText();

      setUrl(text);

      setPasted(true);

      setTimeout(() => {
        setPasted(false);
      }, 1800);

      inputRef.current?.focus();

    } else {

      alert("Clipboard API not supported");
    }

  } catch (err) {

    console.log(err);

    alert(
      "Clipboard access blocked by browser.\nUse CTRL + V inside input."
    );

    inputRef.current?.focus();
  }
};

  const handleDownload = async () => {

    if (!url.trim()) return;

    setStatus("loading");
    setErrorMsg("");
    setDownloadUrl("");
    setProgress(0);

    const interval = setInterval(() => {

      setProgress((prev) => {

        if (prev >= 90) {
          clearInterval(interval);
          return 90;
        }

        return prev + 10;

      });

    }, 300);

    try {

      const response = await fetch(
        `${BASE_URL}/download`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            url: url.trim(),
          }),
        }
      );

      const data = await response.json();

      if (data.success && data.download_url) {

        clearInterval(interval);

        setProgress(100);

        setDownloadUrl(data.download_url);

        setTitle(data.title || "Instagram Reel");

        setThumbnail(data.thumbnail || "");

        setStatus("success");

      } else {

        clearInterval(interval);

        setErrorMsg(
          data.error || "Something went wrong."
        );

        setStatus("error");
      }

    } catch {

      clearInterval(interval);

      setErrorMsg(
        "Unable to reach backend server."
      );

      setStatus("error");
    }
  };

  const handleSave = () => {

    const fullUrl = `${BASE_URL}${downloadUrl}`;

    const a = document.createElement("a");

    a.href = fullUrl;

    a.download = "reel.mp4";

    document.body.appendChild(a);

    a.click();

    document.body.removeChild(a);
  };

  const handleReset = () => {

    setStatus("idle");
    setUrl("");
    setDownloadUrl("");
    setErrorMsg("");
    setThumbnail("");
    setTitle("");
    setProgress(0);

    setTimeout(() => {
      inputRef.current?.focus();
    }, 100);
  };

  return (

    <div className="min-h-screen bg-black text-white flex items-center justify-center px-4 py-10 relative overflow-hidden">

      <GlowOrb className="w-[500px] h-[500px] bg-white top-[-200px] left-[-200px]" />

      <GlowOrb className="w-[400px] h-[400px] bg-white bottom-[-200px] right-[-200px]" />

      <div className="w-full max-w-xl relative z-10">

        <div className="text-center mb-10">

          <div className="flex items-center justify-center gap-2 mb-4">

            <InstagramIcon />

            <span className="text-xs tracking-[0.2em] uppercase text-white/30">
              Reel Downloader
            </span>

          </div>

          <h1 className="text-5xl font-semibold tracking-tight mb-3">
            Save Reels.
          </h1>

          <p className="text-white/30 text-sm">
            Download Instagram reels instantly
          </p>

        </div>

        <div
          className="rounded-3xl border border-white/10 p-6 backdrop-blur-xl"
          style={{
            background:
              "linear-gradient(145deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02))"
          }}
        >

          {
            status === "idle" ||
            status === "error"
              ? (

                <div className="space-y-4">

                  <div className="relative flex items-center gap-3">

                    <input
                      ref={inputRef}
                      type="url"
                      value={url}
                      onChange={(e) => setUrl(e.target.value)}
                      onKeyDown={(e) =>
                        e.key === "Enter" &&
                        isValidUrl &&
                        status !== "loading" &&
                        handleDownload()
                      }
                      placeholder="https://www.instagram.com/reel/..."
                      className="flex-1 rounded-2xl bg-white/5 border border-white/10 px-5 py-4 outline-none"
                    />

                    <button
                      onClick={handlePaste}
                      className="px-4 py-4 rounded-2xl border border-white/10 bg-white/5 hover:bg-white/10 transition text-sm"
                    >
                      {pasted ? "Pasted" : "Paste"}
                    </button>

                  </div>

                  <button
                    onClick={handleDownload}
                    disabled={!isValidUrl}
                    className="w-full bg-white text-black rounded-2xl py-4 font-medium hover:opacity-90 transition disabled:opacity-30"
                  >
                    Download Reel
                  </button>

                  {
                    status === "error" && (

                      <div className="rounded-2xl border border-red-500/20 bg-red-500/5 p-4">

                        <p className="text-red-400 text-sm font-medium mb-1">
                          Download failed
                        </p>

                        <p className="text-white/40 text-xs">
                          {errorMsg}
                        </p>

                      </div>

                    )
                  }

                </div>

              )
              : status === "loading"
                ? (

                  <div className="flex flex-col items-center gap-6 py-8">

                    <Spinner />

                    <div className="w-full">

                      <div className="flex items-center justify-between mb-2">

                        <p className="text-sm text-white/70">
                          Processing Reel
                        </p>

                        <span className="text-xs text-white/30">
                          {progress}%
                        </span>

                      </div>

                      <div className="w-full h-2 rounded-full bg-white/5 overflow-hidden">

                        <div
                          className="h-full bg-white rounded-full transition-all duration-300"
                          style={{
                            width: `${progress}%`
                          }}
                        />

                      </div>

                    </div>

                  </div>

                )
                : (

                  <div className="flex flex-col gap-5">

                    <div className="flex items-center justify-center">
                      <SuccessRing />
                    </div>

                    {
                      thumbnail ? (

                        <div
                          className="w-full overflow-hidden rounded-3xl border border-white/10"
                          style={{
                            background:
                              "linear-gradient(145deg, rgba(255,255,255,0.04), rgba(255,255,255,0.02))"
                          }}
                        >

                          <div
                            className="relative flex items-center justify-center bg-black"
                            style={{
                              minHeight: "320px"
                            }}
                          >

                            <img
                              src={thumbnail}
                              alt="thumbnail"
                              onError={(e) => {
                                e.target.style.display = "none";
                              }}
                              className="w-full max-h-[520px] object-contain bg-black"
                            />

                            <div
                              className="absolute inset-0"
                              style={{
                                background:
                                  "linear-gradient(to top, rgba(0,0,0,0.85), transparent 60%)"
                              }}
                            />

                            <div className="absolute bottom-0 left-0 right-0 p-5">

                              <div
                                className="inline-block px-3 py-1 rounded-full text-xs mb-3"
                                style={{
                                  background: "rgba(255,255,255,0.1)"
                                }}
                              >
                                Instagram Reel
                              </div>

                              <h2 className="text-lg font-semibold">
                                {title}
                              </h2>

                            </div>

                          </div>

                        </div>

                      ) : (

                        <div
                          className="w-full h-64 rounded-3xl flex items-center justify-center border border-white/10"
                          style={{
                            background: "rgba(255,255,255,0.03)"
                          }}
                        >

                          <p className="text-white/30">
                            Preview unavailable
                          </p>

                        </div>

                      )
                    }

                    <button
                      onClick={handleSave}
                      className="w-full rounded-2xl py-4 font-medium border border-white/10 bg-white/5 hover:bg-white/10 transition flex items-center justify-center gap-2"
                    >
                      <DownloadIcon size={16} />
                      Save to Device
                    </button>

                    <button
                      onClick={handleReset}
                      className="text-white/30 text-sm hover:text-white/60 transition"
                    >
                      Download another reel
                    </button>

                  </div>

                )
          }

        </div>

      </div>

    </div>
  );
}