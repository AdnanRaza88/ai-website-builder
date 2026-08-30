# Product Requirements Document

## Project
AI Website Builder — Agentic Spec Driven Development System

## Problem
Building a website requires gathering requirements, writing specs, designing architecture, writing code, and reviewing it. This project automates that pipeline using a coordinated multi agent system that a user drives through a chat interface.

## Goals
1. Let a user describe a website idea in natural language.
2. Agents ask clarifying questions until requirements are complete.
3. Agents produce a PRD and TRD before any code is written.
4. Agents design architecture, then generate real deployable frontend code.
5. Agents review their own output and loop until quality bar is met.
6. User can bring their own LLM provider and API key.
7. User session and memory persist across page reloads.
8. Final output is downloadable as a complete file set.

## Non Goals
- Hosting the generated websites automatically.
- Supporting non web project types in version one.

## Users
Single user per session, identified by a persistent token stored in the browser via URL query parameter.

## Core Flow
1. User opens app, enters or reuses a session token.
2. User selects an LLM provider and pastes an API key in Settings.
3. User describes the website they want.
4. Requirements Agent asks targeted questions until the brief is complete.
5. PRD Agent writes a PRD from the brief.
6. TRD Agent writes a TRD from the PRD.
7. Architect Agent produces a file and component plan.
8. Coder Agent generates the actual HTML, CSS and JS files.
9. Reviewer Agent checks the output against the TRD and either approves or sends it back to the Coder Agent with notes.
10. Loop stops when approved or when the loop limit is hit, whichever comes first.
11. User can download the generated site as a zip.

## Success Criteria
- A user with zero coding knowledge can produce a working static website end to end.
- No agent step silently fails; every failure surfaces a message to the user.
- Session state survives a full page refresh.
