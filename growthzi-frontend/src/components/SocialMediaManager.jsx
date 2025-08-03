import React, { useState, useEffect } from "react";

export default function SocialMediaManager() {
  const backendBaseUrl = "https://ai-social-media-manager-yjgy.onrender.com/api" //"http://localhost:5000/api";

  // Facebook connection
  const [fbStatus, setFbStatus] = useState("Not connected");
  const [fbPageId, setFbPageId] = useState(null);

  // Business profile, errors
  const [businessUrl, setBusinessUrl] = useState("");
  const [businessProfile, setBusinessProfile] = useState(null);
  const [profileError, setProfileError] = useState(null);

  // Industry news, loading, errors
  const [industryNews, setIndustryNews] = useState([]);
  const [newsLoading, setNewsLoading] = useState(false);
  const [newsError, setNewsError] = useState(null);

  // Post generation & preferences
  const [genTone, setGenTone] = useState("motivational");
  const [genType, setGenType] = useState("promo");
  const [genPostCount, setGenPostCount] = useState(3);
  const [genLoading, setGenLoading] = useState(false);
  const [genError, setGenError] = useState(null);

  // Editable generated posts before scheduling
  const [genPostsEditable, setGenPostsEditable] = useState([]);
  const [editingGenIdx, setEditingGenIdx] = useState(null);
  const [editingGenContent, setEditingGenContent] = useState("");

  // Weekly schedule management
  const [schedule, setSchedule] = useState({});
  const [schedFrequency, setSchedFrequency] = useState(3);
  const [schedDays, setSchedDays] = useState(["Mon", "Wed", "Fri"]);
  const [schedError, setSchedError] = useState(null);
  const [schedLoading, setSchedLoading] = useState(false);

  // Publishing
  const [publishStatus, setPublishStatus] = useState(null);

  // Inline edit in schedule
  const [editingDay, setEditingDay] = useState(null);
  const [editContent, setEditContent] = useState("");

  const WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

  // --- Handlers ---

  const connectFacebook = async () => {
    setFbStatus("Connecting...");
    try {
      const res = await fetch(`${backendBaseUrl}/facebook/connect`, { method: "POST" });
      const data = await res.json();
      if (res.ok && data.fb_page_id) {
        setFbStatus(`Connected. Page ID: ${data.fb_page_id}`);
        setFbPageId(data.fb_page_id);
      } else {
        setFbStatus(`Error: ${data.error || "Unknown error"}`);
      }
    } catch (e) {
      setFbStatus(`Error: ${e.message}`);
    }
  };

  const resetAll = () => {
    setProfileError(null);
    setNewsError(null);
    setGenError(null);
    setGenPostsEditable([]);
    setIndustryNews([]);
    setBusinessProfile(null);
    setSchedule({});
    setPublishStatus(null);
    setEditingGenIdx(null);
    setEditingGenContent("");
    setEditingDay(null);
    setEditContent("");
  };

  const handleFullGenerate = async () => {
    resetAll();
    if (!businessUrl.trim()) {
      setProfileError("Please enter a valid business website URL.");
      return;
    }
    try {
      // Fetch business profile
      const profileRes = await fetch(`${backendBaseUrl}/business/profile`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ website_url: businessUrl.trim() }),
      });
      if (!profileRes.ok)
        throw new Error((await profileRes.json()).error || "Failed to fetch profile");
      const profile = (await profileRes.json()).profile;
      setBusinessProfile(profile || {});

      if (!profile.industry) throw new Error("Industry info not found in business profile");

      // Fetch industry news
      setNewsLoading(true);
      setNewsError(null);
      const newsRes = await fetch(`${backendBaseUrl}/news/industry-news`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ industry: profile.industry }),
      });
      if (!newsRes.ok)
        throw new Error((await newsRes.json()).error || "Failed to fetch industry news");
      const newsList = (await newsRes.json()).news || [];
      setIndustryNews(newsList);

      // Generate posts with user count
      setGenLoading(true);
      setGenError(null);
      const payload = {
        name: profile.name || "",
        industry: profile.industry || "",
        tone: genTone,
        post_type: genType,
        news: newsList.map((item) => item.headline || item),
        count: genPostCount,
      };
      const genRes = await fetch(`${backendBaseUrl}/content/generate-posts`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (!genRes.ok) throw new Error((await genRes.json()).error || "Failed to generate posts");
      const posts = (await genRes.json()).posts || [];
      setGenPostsEditable(posts);
    } catch (error) {
      if (error.message.toLowerCase().includes("profile")) setProfileError(error.message);
      else if (error.message.toLowerCase().includes("news")) setNewsError(error.message);
      else if (error.message.toLowerCase().includes("generate")) setGenError(error.message);
      else alert(error.message);
    } finally {
      setNewsLoading(false);
      setGenLoading(false);
    }
  };

  const generateSchedule = async () => {
    if (genPostsEditable.length < schedFrequency) {
      setSchedError("Not enough posts to schedule for chosen days/frequency!");
      return;
    }
    if (schedFrequency > schedDays.length) {
      setSchedError("Post frequency cannot exceed number of preferred days.");
      return;
    }
    setSchedError(null);
    setSchedLoading(true);
    setSchedule({});
    setPublishStatus(null);
    try {
      // 1. POST to create schedule
      const res = await fetch(`${backendBaseUrl}/weekly-planner/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          post_frequency: schedFrequency,
          preferred_days: schedDays,
        }),
      });
      if (!res.ok) {
        const err = await res.json();
        setSchedError(err.error || "Failed to generate schedule.");
        setSchedLoading(false);
        return;
      }
      // 2. PUT to update days with generated posts
      const chosenDays = schedDays.slice(0, schedFrequency);
      for (const [i, day] of chosenDays.entries()) {
        await fetch(`${backendBaseUrl}/weekly-planner/${day}`, {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ content: genPostsEditable[i] }),
        });
      }
      // 3. Get latest schedule
      const schedRes = await fetch(`${backendBaseUrl}/weekly-planner/`);
      const schedData = await schedRes.json();
      setSchedule(schedData);
    } catch (e) {
      setSchedError(e.message);
    } finally {
      setSchedLoading(false);
    }
  };

  useEffect(() => {
    (async () => {
      try {
        const res = await fetch(`${backendBaseUrl}/weekly-planner/`);
        if (res.ok) {
          const data = await res.json();
          setSchedule(data);
        }
      } catch {
        // ignore
      }
    })();
  }, []);

  const updatePost = async (day, newContent) => {
    try {
      const res = await fetch(`${backendBaseUrl}/weekly-planner/${day}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ content: newContent }),
      });
      const data = await res.json();
      if (res.ok) setSchedule(data);
      else alert(data.error || "Failed to update post.");
    } catch (e) {
      alert(e.message);
    }
  };

  const deletePost = async (day) => {
    if (!window.confirm(`Delete post scheduled for ${day}?`)) return;
    try {
      const res = await fetch(`${backendBaseUrl}/weekly-planner/${day}`, { method: "DELETE" });
      const data = await res.json();
      if (res.ok) setSchedule(data);
      else alert(data.error || "Failed to delete post.");
    } catch (e) {
      alert(e.message);
    }
  };

  const startEditing = (day) => {
    setEditingDay(day);
    setEditContent(schedule[day]);
  };
  const saveEdit = () => {
    updatePost(editingDay, editContent);
    setEditingDay(null);
    setEditContent("");
  };
  const cancelEdit = () => {
    setEditingDay(null);
    setEditContent("");
  };

  const publishPost = async (day) => {
    if (!fbPageId) {
      alert("Connect your Facebook page first.");
      return;
    }
    try {
      setPublishStatus("Publishing...");
      const res = await fetch(`${backendBaseUrl}/facebook/publish`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ page_id: fbPageId, day, content: schedule[day] }),
      });
      const data = await res.json();
      if (res.ok) setPublishStatus(data);
      else setPublishStatus(data.error || "Publish failed");
    } catch (e) {
      setPublishStatus(`Publish error: ${e.message}`);
    }
  };

  const renderGeneratedPostsEditable = () => (
    <section>
      <h3>Generated Posts Preview (Edit or Delete before scheduling)</h3>
      <ol>
        {genPostsEditable.map((post, idx) => (
          <li key={idx} style={{ marginBottom: "10px" }}>
            {editingGenIdx === idx ? (
              <>
                <textarea
                  rows={3}
                  value={editingGenContent}
                  onChange={(e) => setEditingGenContent(e.target.value)}
                />
                <button
                  onClick={() => {
                    const newPosts = [...genPostsEditable];
                    newPosts[idx] = editingGenContent;
                    setGenPostsEditable(newPosts);
                    setEditingGenIdx(null);
                    setEditingGenContent("");
                  }}
                >
                  Save
                </button>
                <button onClick={() => { setEditingGenIdx(null); setEditingGenContent(""); }}>
                  Cancel
                </button>
              </>
            ) : (
              <>
                {post}
                <button style={{ marginLeft: 10 }} onClick={() => { setEditingGenIdx(idx); setEditingGenContent(post); }}>
                  Edit
                </button>
                <button
                  style={{ marginLeft: 6 }}
                  onClick={() => setGenPostsEditable(genPostsEditable.filter((_, i) => i !== idx))}
                >
                  Delete
                </button>
              </>
            )}
          </li>
        ))}
      </ol>
    </section>
  );

  const renderBusinessProfile = () => {
    if (!businessProfile) return null;
    return (
      <div className="profile-friendly">
        <h3>Business Profile</h3>
        <p><strong>Name:</strong> {businessProfile.name || "N/A"}</p>
        <p><strong>Industry:</strong> {businessProfile.industry || "N/A"}</p>
        <p>
          <strong>Services:</strong>{" "}
          {Array.isArray(businessProfile.services)
            ? businessProfile.services.join(", ")
            : businessProfile.services || "N/A"}
        </p>
        <p><strong>Tone of Voice:</strong> {businessProfile.tone_of_voice || "N/A"}</p>
        {businessProfile.unique_value_proposition && (
          <p><strong>Unique Value Proposition:</strong> {businessProfile.unique_value_proposition}</p>
        )}
      </div>
    );
  };

  return (
    <div className="container">
      <h1>Growthzi AI Social Media Manager</h1>

      <section>
        <button onClick={connectFacebook}>Connect Facebook</button>
        <div className="status">{fbStatus}</div>
      </section>

      <section>
        <label htmlFor="businessUrl">Business Website URL:</label>
        <input
          id="businessUrl"
          type="url"
          placeholder="https://example.com"
          value={businessUrl}
          onChange={e => setBusinessUrl(e.target.value)}
          disabled={genLoading || newsLoading}
        />
        <label>
          Tone:
          <select value={genTone} onChange={e => setGenTone(e.target.value)}>
            <option value="motivational">Motivational</option>
            <option value="professional">Professional</option>
            <option value="fun">Fun</option>
            <option value="informative">Informative</option>
          </select>
        </label>
        <label>
          Post Type:
          <select value={genType} onChange={e => setGenType(e.target.value)}>
            <option value="promo">Promotional</option>
            <option value="business_tips">Business Tips</option>
            <option value="industry_insights">Industry Insights</option>
            <option value="seasonal">Seasonal</option>
            <option value="general">General</option>
          </select>
        </label>
        <label>
          Number of Posts to Generate:
          <input
            type="number"
            min={1}
            max={10}
            style={{ width: 60, marginLeft: 7 }}
            value={genPostCount}
            onChange={e => setGenPostCount(parseInt(e.target.value) || 1)}
            disabled={genLoading || newsLoading}
          />
        </label>
        <button onClick={handleFullGenerate} disabled={genLoading || newsLoading}>
          {genLoading || newsLoading ? "Processing..." : "Generate Posts (Full Flow)"}
        </button>
        {profileError && <div className="error">{profileError}</div>}
        {newsError && <div className="error">{newsError}</div>}
        {genError && <div className="error">{genError}</div>}
        {renderBusinessProfile()}
      </section>

      {industryNews.length > 0 && (
        <section>
          <h3>Industry News</h3>
          <ul>
            {industryNews.map((item, idx) => (
              <li key={idx}>
                {item.headline || item}
                {item.url && (
                  <a href={item.url} target="_blank" rel="noreferrer noopener">
                    {" "} [Read More]
                  </a>
                )}
              </li>
            ))}
          </ul>
        </section>
      )}

      {genPostsEditable.length > 0 && renderGeneratedPostsEditable()}

      {genPostsEditable.length > 0 && (
        <section>
          <h3>Schedule Your Posts</h3>
          <label>
            Post Frequency:
            <input
              type="number"
              min={1}
              max={7}
              value={schedFrequency}
              onChange={e => setSchedFrequency(parseInt(e.target.value) || 1)}
            />
          </label>
          <label>
            Preferred Days:
            <select
              multiple
              value={schedDays}
              onChange={e =>
                setSchedDays(Array.from(e.target.selectedOptions, (opt) => opt.value))
              }
              size={7}
            >
              {WEEKDAYS.map(day => (
                <option key={day} value={day}>{day}</option>
              ))}
            </select>
            <small>Ctrl+click to select multiple</small>
          </label>
          <button onClick={generateSchedule} disabled={schedLoading}>
            {schedLoading ? "Scheduling..." : "Generate Weekly Schedule"}
          </button>
          {schedError && <div className="error">{schedError}</div>}
        </section>
      )}

      {Object.keys(schedule).length > 0 && (
        <section>
          <h3>Weekly Scheduled Posts</h3>
          <table className="schedule-table">
            <thead>
              <tr>
                <th>Day</th>
                <th>Post Content</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {WEEKDAYS.filter(day => schedule[day]).map(day => (
                <tr key={day}>
                  <td>{day}</td>
                  <td>
                    {editingDay === day ? (
                      <textarea
                        rows={3}
                        value={editContent}
                        onChange={e => setEditContent(e.target.value)}
                      />
                    ) : (
                      schedule[day]
                    )}
                  </td>
                  <td>
                    {editingDay === day ? (
                      <>
                        <button onClick={saveEdit}>Save</button>
                        <button onClick={cancelEdit}>Cancel</button>
                      </>
                    ) : (
                      <>
                        <button onClick={() => startEditing(day)}>Edit</button>
                        <button onClick={() => deletePost(day)}>Delete</button>
                        <button onClick={() => publishPost(day)}>Publish</button>
                      </>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {publishStatus && typeof publishStatus === "object" ? (
            <div className="publish-status">
              <b>Published successfully!</b><br />
              <a href={publishStatus.post_link || publishStatus.post_url}
                 target="_blank"
                 rel="noopener noreferrer">
                {publishStatus.post_link || publishStatus.post_url}
              </a>
            </div>
          ) : (
            publishStatus && <div className="publish-status">{publishStatus}</div>
          )}
        </section>
      )}
    </div>
  );
}
