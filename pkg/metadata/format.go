// Copyright 2025 Notedown Authors
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

package metadata

import (
	"log/slog"
	"strings"

	"github.com/notedownorg/notedown/pkg/providers/source"
)

// Kind is used for later processing
// e.g. if YouTube we need to use a specific method for downloading the video
type Kind string

const (
	YouTube       Kind = "YouTube"
	NotApplicable Kind = "NotApplicable"
)

func InferFormat(url string) (source.Format, Kind, error) {
	if strings.Contains(url, "youtube.com") || strings.Contains(url, "youtu.be") {
		slog.Info("detected YouTube video", "url", url)
		return source.Video, YouTube, nil
	}

	slog.Info("no format detected, assuming text article", "url", url)
	return source.Article, NotApplicable, nil
}
