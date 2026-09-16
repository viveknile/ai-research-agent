const API_URL =
  process.env.NEXT_PUBLIC_API_URL ||
  "http://localhost:8000/api/v1";


export type ResearchDepth =
  | "quick"
  | "standard"
  | "deep";


export type ResearchStatus =
  | "running"
  | "completed"
  | "failed";


export interface ResearchRequest {
  query: string;
  depth: ResearchDepth;
}


export interface ResearchResponse {
  research_id: string;
  status: string;
}


export interface ResearchResult {
  research_id: string;
  query: string;
  depth: ResearchDepth;

  status: ResearchStatus;

  progress: number;
  step: number;

  current_step: string;
  current_description: string;

  result: Record<string, unknown> | null;

  error: string | null;
}


/**
 * Start a new research job.
 */
export async function createResearch(
  request: ResearchRequest,
): Promise<ResearchResponse> {

  const response = await fetch(
    `${API_URL}/research`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify(request),
    },
  );


  if (!response.ok) {

    let message =
      "Failed to start research.";

    try {

      const data =
        await response.json();

      if (data?.detail) {
        message = data.detail;
      }

    } catch {
      // Ignore JSON parsing errors.
    }

    throw new Error(message);
  }


  return response.json();
}


/**
 * Get the current status/result
 * of a research job.
 */
export async function getResearch(
  researchId: string,
): Promise<ResearchResult> {

  const response = await fetch(
    `${API_URL}/research/${researchId}`,
    {
      method: "GET",
      cache: "no-store",
    },
  );


  if (!response.ok) {

    let message =
      "Failed to get research status.";

    try {

      const data =
        await response.json();

      if (data?.detail) {
        message = data.detail;
      }

    } catch {
      // Ignore JSON parsing errors.
    }

    throw new Error(message);
  }


  return response.json();
}