{{/*
Expand the name of the chart.
*/}}
{{- define "k10animalai.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "k10animalai.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "k10animalai.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "k10animalai.labels" -}}
helm.sh/chart: {{ include "k10animalai.chart" . }}
{{ include "k10animalai.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "k10animalai.selectorLabels" -}}
app.kubernetes.io/name: {{ include "k10animalai.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "k10animalai.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "k10animalai.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
Return the proper image name
*/}}
{{- define "k10animalai.image" -}}
{{- printf "%s/%s/%s:%s" .Values.k10animalai.image.registry .Values.k10animalai.image.repository .Values.k10animalai.image.image .Values.k10animalai.image.tag }}
{{- end }}

{{/*
Ingress API version helper
*/}}
{{- define "ingress.apiVersion" -}}
{{- if semverCompare ">=1.19-0" .Capabilities.KubeVersion.GitVersion -}}
networking.k8s.io/v1
{{- else if semverCompare ">=1.14-0" .Capabilities.KubeVersion.GitVersion -}}
networking.k8s.io/v1beta1
{{- else -}}
extensions/v1beta1
{{- end -}}
{{- end }}

{{/*
Check if ingress is stable
*/}}
{{- define "ingress.isStable" -}}
{{- eq (include "ingress.apiVersion" .) "networking.k8s.io/v1" -}}
{{- end }}

{{/*
Ingress class annotation helper
*/}}
{{- define "ingressClassAnnotation" -}}
{{- if .Values.ingress.class -}}
kubernetes.io/ingress.class: {{ .Values.ingress.class }}
{{- end -}}
{{- end }}

{{/*
App URL path helper
*/}}
{{- define "app.urlPath" -}}
{{- default "/" .Values.ingress.path -}}
{{- end }}

{{/*
Qdrant host helper - returns the appropriate service name
*/}}
{{- define "k10animalai.qdrantHost" -}}
{{- if .Values.qdrant.enabled -}}
{{- printf "%s-qdrant" .Release.Name -}}
{{- else -}}
{{- .Values.qdrant.host -}}
{{- end -}}
{{- end }}
