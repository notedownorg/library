// Copyright 2024 Notedown Authors
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

package notedown

import (
	"time"

	"github.com/notedownorg/notedown/pkg/configuration"
	"github.com/notedownorg/notedown/pkg/providers/source"
	"github.com/notedownorg/notedown/pkg/workspace/reader"
	"github.com/notedownorg/notedown/pkg/workspace/writer"
)

type SourceWriter interface {
	CreateSource(title string, format source.Format, url string, options ...source.SourceOption) error
}

type Client interface {
	SourceWriter
}

type client struct {
	*source.SourceClient
}

func NewClient(workspace *configuration.Workspace) (Client, error) {
	cfg, err := configuration.EnsureWorkspaceConfiguration(workspace.Location)
	if err != nil {
		return nil, err
	}

	read, err := reader.NewClient(workspace, "library")
	if err != nil {
		return nil, err
	}
	write := writer.NewClient(workspace)

	sourceReaderChannel := make(chan reader.Event)
	read.Subscribe(sourceReaderChannel, reader.WithInitialDocuments())
	sourceClient := source.NewClient(&cfg.Sources, write, sourceReaderChannel, source.WithInitialLoadWaiter(100*time.Millisecond))

	return &client{
		SourceClient: sourceClient,
	}, nil
}
