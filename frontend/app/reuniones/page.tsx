"use client";

import { useState, useEffect, useRef } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Sidebar } from "@/components/ui/sidebar";
import { useTranslation } from "@/lib/i18n";
import {
  Calendar, Clock, Plus, Mic, FileText,
  Play, Square, Trash2, Download, X, StopCircle,
} from "lucide-react";

interface Meeting {
  id: string; title: string; date: string; duration: number;
  status: string; transcript?: string; summary?: string;
  participants?: string; recording_url?: string; recording_duration?: number;
}

export default function ReunionesPage() {
  const { t } = useTranslation();
  const [meetings, setMeetings] = useState<Meeting[]>([]);
  const [loading, setLoading] = useState(true);
  const [showCreate, setShowCreate] = useState(false);
  const [recording, setRecording] = useState(false);
  const [recordingMeetingId, setRecordingMeetingId] = useState<string | null>(null);
  const [recordingTime, setRecordingTime] = useState(0);
  const mediaRecorder = useRef<MediaRecorder | null>(null);
  const audioChunks = useRef<Blob[]>([]);
  const timerRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    fetchMeetings();
  }, []);

  const fetchMeetings = async () => {
    const token = localStorage.getItem("access_token");
    if (!token) return;
    try {
      const res = await fetch("/api/meetings/", {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (res.ok) setMeetings(await res.json());
    } finally {
      setLoading(false);
    }
  };

  const createMeeting = async (e: React.FormEvent) => {
    e.preventDefault();
    const form = e.target as HTMLFormElement;
    const token = localStorage.getItem("access_token");
    const data = {
      title: (form.elements.namedItem("title") as HTMLInputElement).value,
      date: new Date((form.elements.namedItem("date") as HTMLInputElement).value).toISOString(),
      duration: parseInt((form.elements.namedItem("duration") as HTMLInputElement).value) || 60,
      participants: (form.elements.namedItem("participants") as HTMLInputElement).value,
    };
    const res = await fetch("/api/meetings/", {
      method: "POST",
      headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
      body: JSON.stringify(data),
    });
    if (res.ok) {
      setShowCreate(false);
      fetchMeetings();
    }
  };

  const deleteMeeting = async (id: string) => {
    if (!confirm(t("meetings.delete_confirm"))) return;
    const token = localStorage.getItem("access_token");
    await fetch(`/api/meetings/${id}`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${token}` },
    });
    fetchMeetings();
  };

  const startRecording = async (meetingId: string) => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream, { mimeType: "audio/webm" });
      mediaRecorder.current = recorder;
      audioChunks.current = [];
      setRecordingMeetingId(meetingId);
      setRecording(true);
      setRecordingTime(0);

      recorder.ondataavailable = (e) => {
        if (e.data.size > 0) audioChunks.current.push(e.data);
      };

      recorder.onstop = async () => {
        stream.getTracks().forEach((t) => t.stop());
        const blob = new Blob(audioChunks.current, { type: "audio/webm" });
        const token = localStorage.getItem("access_token");
        const formData = new FormData();
        formData.append("file", blob, `recording_${meetingId}.webm`);
        await fetch(`/api/meetings/${meetingId}/recording`, {
          method: "POST",
          headers: { Authorization: `Bearer ${token}` },
          body: formData,
        });
        setRecording(false);
        setRecordingMeetingId(null);
        if (timerRef.current) clearInterval(timerRef.current);
        fetchMeetings();
      };

      recorder.start(1000);
      timerRef.current = setInterval(() => setRecordingTime((t) => t + 1), 1000);
    } catch {
      alert(t("meetings.mic_error"));
    }
  };

  const stopRecording = () => {
    if (mediaRecorder.current && mediaRecorder.current.state !== "inactive") {
      mediaRecorder.current.stop();
    }
  };

  const formatTime = (s: number) => {
    const m = Math.floor(s / 60);
    const sec = s % 60;
    return `${m}:${sec.toString().padStart(2, "0")}`;
  };

  const formatDuration = (min: number) => {
    if (min >= 60) return `${Math.floor(min / 60)}h ${min % 60}m`;
    return `${min}m`;
  };

  return (
    <Sidebar>
      <div className="p-6 space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold">{t("meetings.title")}</h1>
            <p className="text-sm text-muted-foreground">{t("meetings.subtitle")}</p>
          </div>
          <div className="flex gap-2">
            <Button size="sm" onClick={() => setShowCreate(true)}>
              <Plus className="mr-2 h-4 w-4" />
              {t("meetings.new")}
            </Button>
          </div>
        </div>

        {recording && (
          <div className="flex items-center gap-3 rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
            <div className="h-3 w-3 animate-pulse rounded-full bg-red-500" />
            <span className="font-medium">{t("meetings.recording_in_progress")}</span>
            <span className="font-mono">{formatTime(recordingTime)}</span>
            <Button size="sm" variant="destructive" onClick={stopRecording} className="ml-auto">
              <StopCircle className="mr-1 h-4 w-4" />
              {t("meetings.stop")}
            </Button>
          </div>
        )}

        <Card>
          <CardContent className="p-0">
            {loading ? (
              <p className="p-4 text-sm text-muted-foreground">{t("meetings.loading")}</p>
            ) : meetings.length === 0 ? (
              <p className="p-4 text-sm text-muted-foreground">{t("meetings.no_meetings")}</p>
            ) : (
              <div className="divide-y">
                {meetings.map((meeting) => (
                  <div key={meeting.id} className="flex items-center justify-between p-4 hover:bg-muted/50 transition-colors">
                    <div className="flex items-start gap-4 flex-1">
                      <div className="rounded-lg bg-blue-100 p-2 mt-1">
                        <Calendar className="h-4 w-4 text-blue-600" />
                      </div>
                      <div className="flex-1">
                        <p className="font-medium">{meeting.title}</p>
                        <div className="flex items-center gap-3 mt-1 text-xs text-muted-foreground">
                          <span className="flex items-center gap-1">
                            <Clock className="h-3 w-3" />
                            {new Date(meeting.date).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
                          </span>
                          <span>{new Date(meeting.date).toLocaleDateString()}</span>
                          <span>{formatDuration(meeting.duration)}</span>
                          <span>{meeting.participants || "0"} {t("meetings.participants")}</span>
                        </div>
                        {meeting.summary && (
                          <p className="text-xs text-muted-foreground mt-2 italic">{meeting.summary}</p>
                        )}
                        {meeting.recording_url && (
                          <div className="mt-2">
                            <audio controls className="h-8 w-64" preload="none">
                              <source src={meeting.recording_url} type="audio/webm" />
                            </audio>
                          </div>
                        )}
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <Badge variant={
                        meeting.status === "completed" ? "success" :
                        meeting.status === "scheduled" ? "secondary" : "destructive"
                      }>
                        {meeting.status === "completed" ? t("meetings.completed") :
                         meeting.status === "scheduled" ? t("meetings.scheduled") : t("meetings.cancelled")}
                      </Badge>
                      {meeting.status === "scheduled" && !recording && (
                        <Button variant="outline" size="sm" onClick={() => startRecording(meeting.id)}>
                          <Mic className="h-4 w-4" />
                        </Button>
                      )}
                      <Button variant="ghost" size="sm" onClick={() => deleteMeeting(meeting.id)}>
                        <Trash2 className="h-4 w-4 text-red-500" />
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {showCreate && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50" onClick={() => setShowCreate(false)}>
          <div className="w-full max-w-md rounded-2xl bg-white p-8 shadow-2xl" onClick={(e) => e.stopPropagation()}>
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-bold">{t("meetings.new")}</h2>
              <button onClick={() => setShowCreate(false)}><X className="h-5 w-5" /></button>
            </div>
            <form onSubmit={createMeeting} className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">{t("meetings.title_label")}</label>
                <input name="title" className="w-full rounded-lg border px-4 py-2 text-sm" required />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">{t("meetings.date_label")}</label>
                <input name="date" type="datetime-local" className="w-full rounded-lg border px-4 py-2 text-sm" required />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">{t("meetings.duration_label")}</label>
                <input name="duration" type="number" defaultValue="60" className="w-full rounded-lg border px-4 py-2 text-sm" />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">{t("meetings.participants_label")}</label>
                <input name="participants" placeholder="ej: Juan, María, Pedro" className="w-full rounded-lg border px-4 py-2 text-sm" />
              </div>
              <Button type="submit" className="w-full">{t("meetings.create")}</Button>
            </form>
          </div>
        </div>
      )}
    </Sidebar>
  );
}
